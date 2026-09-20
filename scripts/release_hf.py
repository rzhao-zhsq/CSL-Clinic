"""Publish the validated CSL-Clinic test split to Hugging Face.

The script is dry-run by default. Pass ``--apply`` to create the release
commit and ``--super-squash`` to remove the previous train/dev file history.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from huggingface_hub import CommitOperationAdd, CommitOperationDelete, HfApi


@dataclass(frozen=True)
class LocalVideo:
    remote_path: str
    local_path: Path
    size: int


def default_card_path() -> Path:
    script_path = Path(__file__).resolve()
    candidates = [
        script_path.parents[1] / "huggingface" / "README.md",
        script_path.parent / "README.md",
    ]
    return next((path for path in candidates if path.is_file()), candidates[0])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", default="rzhao/CSL-Clinic")
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path(r"F:\workspace\data\SignLanguage\CSL-Clinic\hf_csl_clinic"),
    )
    parser.add_argument(
        "--card",
        type=Path,
        default=default_card_path(),
    )
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--super-squash", action="store_true")
    return parser.parse_args()


def build_local_release(data_root: Path) -> tuple[Path, dict[str, LocalVideo]]:
    metadata_path = data_root / "test" / "metadata.csv"
    if not metadata_path.is_file():
        raise FileNotFoundError(f"Missing test metadata: {metadata_path}")

    with metadata_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 500:
        raise ValueError(f"Expected 500 test rows, found {len(rows)}")
    if set(rows[0]) != {"file_name", "gloss", "text"}:
        raise ValueError(f"Unexpected metadata columns: {list(rows[0])}")

    videos: dict[str, LocalVideo] = {}
    for row in rows:
        relative = PurePosixPath(row["file_name"])
        if relative.parent != PurePosixPath("video") or relative.suffix.lower() != ".mp4":
            raise ValueError(f"Unexpected test video path: {relative}")

        candidates = [
            data_root / split / Path(*relative.parts)
            for split in ("test", "train", "dev")
        ]
        matches = [path for path in candidates if path.is_file()]
        if len(matches) != 1:
            raise ValueError(
                f"Expected exactly one source for {relative}, found {len(matches)}: {matches}"
            )

        remote_path = f"test/{relative.as_posix()}"
        if remote_path in videos:
            raise ValueError(f"Duplicate metadata path: {remote_path}")
        videos[remote_path] = LocalVideo(
            remote_path=remote_path,
            local_path=matches[0],
            size=matches[0].stat().st_size,
        )

    return metadata_path, videos


def list_remote_files(api: HfApi, repo_id: str) -> dict[str, int | None]:
    files: dict[str, int | None] = {}
    for item in api.list_repo_tree(
        repo_id=repo_id,
        repo_type="dataset",
        recursive=True,
        expand=False,
    ):
        if hasattr(item, "size"):
            files[item.path] = item.size
    return files


def validate_remote(
    api: HfApi,
    repo_id: str,
    expected_videos: dict[str, LocalVideo],
) -> None:
    remote = list_remote_files(api, repo_id)
    expected = set(expected_videos) | {"README.md", "test/metadata.csv", ".gitattributes"}
    missing = sorted(set(expected_videos) - set(remote))
    unexpected = sorted(set(remote) - expected)
    wrong_sizes = sorted(
        path
        for path, video in expected_videos.items()
        if path in remote and remote[path] is not None and remote[path] != video.size
    )
    if missing or unexpected or wrong_sizes:
        raise RuntimeError(
            "Remote validation failed: "
            f"missing={len(missing)}, unexpected={len(unexpected)}, "
            f"wrong_sizes={len(wrong_sizes)}"
        )
    print(
        "Remote validation passed: "
        f"videos={len(expected_videos)}, total_files={len(remote)}"
    )


def main() -> None:
    args = parse_args()
    metadata_path, videos = build_local_release(args.data_root)
    if not args.card.is_file():
        raise FileNotFoundError(f"Missing dataset card: {args.card}")

    api = HfApi()
    remote = list_remote_files(api, args.repo_id)
    target_videos = set(videos)
    remote_test_videos = {
        path for path in remote if path.startswith("test/video/")
    }
    extra_test_videos = sorted(remote_test_videos - target_videos)
    uploads = sorted(
        (
            video
            for video in videos.values()
            if video.remote_path not in remote
            or (
                remote[video.remote_path] is not None
                and remote[video.remote_path] != video.size
            )
        ),
        key=lambda video: video.remote_path,
    )

    delete_train = any(path.startswith("train/") for path in remote)
    delete_dev = any(path.startswith("dev/") for path in remote)

    print(f"Local test metadata rows: {len(videos)}")
    print(f"Remote files before release: {len(remote)}")
    print(f"Delete train directory: {delete_train}")
    print(f"Delete dev directory: {delete_dev}")
    print(f"Delete unreferenced test videos: {len(extra_test_videos)}")
    print(f"Upload missing or size-mismatched test videos: {len(uploads)}")
    for path in extra_test_videos:
        print(f"  DELETE {path}")
    for video in uploads:
        print(f"  UPLOAD {video.local_path} -> {video.remote_path}")

    if not args.apply:
        print("Dry run only. Re-run with --apply after reviewing this plan.")
        return

    operations = []
    if delete_train:
        operations.append(CommitOperationDelete(path_in_repo="train/", is_folder=True))
    if delete_dev:
        operations.append(CommitOperationDelete(path_in_repo="dev/", is_folder=True))
    operations.extend(
        CommitOperationDelete(path_in_repo=path) for path in extra_test_videos
    )
    operations.extend(
        [
            CommitOperationAdd(path_in_repo="README.md", path_or_fileobj=args.card),
            CommitOperationAdd(
                path_in_repo="test/metadata.csv", path_or_fileobj=metadata_path
            ),
        ]
    )
    operations.extend(
        CommitOperationAdd(
            path_in_repo=video.remote_path,
            path_or_fileobj=video.local_path,
        )
        for video in uploads
    )

    commit = api.create_commit(
        repo_id=args.repo_id,
        repo_type="dataset",
        operations=operations,
        commit_message="Release public CSL-Clinic test split",
    )
    print(f"Created release commit: {commit.commit_url}")

    validate_remote(api, args.repo_id, videos)

    if args.super_squash:
        api.super_squash_history(repo_id=args.repo_id, repo_type="dataset")
        print("Super-squashed repository history.")
        validate_remote(api, args.repo_id, videos)


if __name__ == "__main__":
    main()
