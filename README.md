# CSL-Clinic

[![Paper](https://img.shields.io/badge/IJCV-Paper-blue)](https://link.springer.com/article/10.1007/s11263-026-02978-x)
[![Dataset](https://img.shields.io/badge/Hugging%20Face-Dataset-yellow)](https://huggingface.co/datasets/rzhao/CSL-Clinic)
[![Code](https://img.shields.io/badge/Code-CV--SLT-green)](https://github.com/rzhao-zhsq/CV-SLT)

CSL-Clinic is a gloss-annotated Chinese Sign Language dataset for sign language understanding in the clinical and healthcare domain. It was introduced in our IJCV paper, [Variational Sign Language Translation](https://link.springer.com/article/10.1007/s11263-026-02978-x).

## News

- **[Sep. 2026]** We released the 500-example test split on [Hugging Face](https://huggingface.co/datasets/rzhao/CSL-Clinic). The complete dataset is available for research use upon request.
- **[Aug. 2026]** Our paper was accepted by the *International Journal of Computer Vision* (IJCV) and published online.

## Dataset Overview

CSL-Clinic contains 5,972 sign-language videos. Every example is aligned with a gloss sequence and a Chinese sentence.

| Split | Examples | Public availability |
| --- | ---: | --- |
| Train | 5,000 | Available by request |
| Dev | 472 | Available by request |
| Test | 500 | [Public on Hugging Face](https://huggingface.co/datasets/rzhao/CSL-Clinic) |
| **Total** | **5,972** |  |

Each annotation has the following fields:

| Field | Description |
| --- | --- |
| `file_name` | Relative path to the sign-language video |
| `gloss` | Segmented sign gloss sequence |
| `text` | Corresponding Chinese natural-language sentence |

## Public Test Split

The public release contains only the test split:

```text
test/
├── metadata.csv
└── video/
    ├── example_0001.mp4
    └── ...
```

Download it from the [CSL-Clinic Hugging Face repository](https://huggingface.co/datasets/rzhao/CSL-Clinic):

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="rzhao/CSL-Clinic",
    repo_type="dataset",
    local_dir="CSL-Clinic",
)
```

## Requesting the Complete Dataset

The train and dev splits are not distributed publicly. Researchers who need the complete dataset should follow the instructions in [DATA_REQUEST.md](DATA_REQUEST.md) and email the corresponding author at [ydchen@xmu.edu.cn](mailto:ydchen@xmu.edu.cn).

Please do not redistribute any non-public portion of CSL-Clinic or attempt to identify the signers.

## Intended Uses and Limitations

CSL-Clinic supports research on:

- continuous sign language recognition;
- sign language translation;
- gloss-to-text translation;
- multimodal learning for accessible medical communication.

The dataset does not cover every Chinese Sign Language variant, signer style, medical specialty, or recording condition. Models trained or evaluated on CSL-Clinic can make consequential errors and must not be used as a substitute for professional medical advice, diagnosis, emergency communication, or qualified human interpretation.

## Related Resources

- [IJCV paper](https://link.springer.com/article/10.1007/s11263-026-02978-x)
- [CV-SLT/VSLT implementation](https://github.com/rzhao-zhsq/CV-SLT)
- [Hugging Face dataset](https://huggingface.co/datasets/rzhao/CSL-Clinic)

## Citation

If you use CSL-Clinic, please cite:

```bibtex
@article{zhao2026variational,
  title   = {Variational Sign Language Translation},
  author  = {Zhao, Rui and Zhang, Liang and Fu, Biao and Zhang, Ruiquan and Chen, Yidong and Shi, Xiaodong},
  journal = {International Journal of Computer Vision},
  volume  = {134},
  pages   = {408},
  year    = {2026},
  doi     = {10.1007/s11263-026-02978-x},
  url     = {https://doi.org/10.1007/s11263-026-02978-x}
}
```

## Contact

For dataset-access requests, use the template in [DATA_REQUEST.md](DATA_REQUEST.md). For other questions, please open a GitHub issue.
