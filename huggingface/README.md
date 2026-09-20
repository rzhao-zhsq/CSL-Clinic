---
pretty_name: CSL-Clinic
language:
- zh
tags:
- sign-language
- sign-language-translation
- sign-language-recognition
- chinese-sign-language
- medical
- healthcare
- video
- gloss
size_categories:
- n<1K
---

# Dataset Card for CSL-Clinic

CSL-Clinic is a gloss-annotated Chinese Sign Language dataset for sign language understanding in the clinical and healthcare domain. It was introduced in [Variational Sign Language Translation](https://link.springer.com/article/10.1007/s11263-026-02978-x), published in the *International Journal of Computer Vision*.

## Public Release and Full-Dataset Access

This Hugging Face repository publicly distributes **only the 500-example test split**. The complete dataset contains 5,972 examples; its train and dev splits are available to researchers upon request.

| Split | Examples | Availability |
| --- | ---: | --- |
| train | 5,000 | Available by email request |
| dev | 472 | Available by email request |
| test | 500 | Public in this repository |
| **Total** | **5,972** |  |

To request the complete dataset, follow the instructions in the [GitHub repository](https://github.com/rzhao-zhsq/CSL-Clinic/blob/main/DATA_REQUEST.md) and email the corresponding author at [ydchen@xmu.edu.cn](mailto:ydchen@xmu.edu.cn).

## Dataset Structure

```text
test/
├── metadata.csv
└── video/
    ├── example_0001.mp4
    └── ...
```

The public split contains 500 MP4 videos and one annotation row per video.

### Data Fields

- `file_name`: relative path to the video inside the test directory;
- `gloss`: segmented Chinese Sign Language gloss sequence;
- `text`: corresponding Chinese natural-language sentence.

## Intended Uses

CSL-Clinic supports research on continuous sign language recognition, sign language translation, gloss-to-text translation, multimodal learning, and accessible medical communication.

## Out-of-Scope Uses

The dataset must not be used as a substitute for professional medical advice, diagnosis, emergency communication, or qualified human interpretation. Models trained or evaluated on this dataset may produce consequential recognition or translation errors.

## Limitations and Privacy

- The dataset may not cover every Chinese Sign Language variant, signer style, medical specialty, or recording condition.
- Performance on CSL-Clinic may not generalize to real clinical environments.
- Video quality, signer identity, background, and recording conditions may affect model behavior.
- Users should not attempt to identify signers or infer private personal attributes.
- Non-public portions of the dataset must not be redistributed.

## Citation

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

## Links

- [Project repository](https://github.com/rzhao-zhsq/CSL-Clinic)
- [Paper](https://link.springer.com/article/10.1007/s11263-026-02978-x)
- [Implementation](https://github.com/rzhao-zhsq/CV-SLT)
