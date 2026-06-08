# Citation

If you use this repository, please cite the underlying dataset and tooling. The
**dataset license is separate from this repository's code license** (see
[Licensing](#licensing) below).

## What to cite

1. **The PhysioNet EEG Motor Movement/Imagery Dataset** (acquired with BCI2000).
2. **PhysioNet / PhysioBank** (the platform that hosts and distributes the data).
3. **MNE-Python** (the analysis library used to load and process the data).

---

## BibTeX

```bibtex
@article{schalk2004bci2000,
  author  = {Schalk, Gerwin and McFarland, Dennis J. and Hinterberger, Thilo
             and Birbaumer, Niels and Wolpaw, Jonathan R.},
  title   = {{BCI2000}: A General-Purpose Brain-Computer Interface ({BCI})
             System},
  journal = {IEEE Transactions on Biomedical Engineering},
  volume  = {51},
  number  = {6},
  pages   = {1034--1043},
  year    = {2004},
  doi     = {10.1109/TBME.2004.827072}
}

@article{goldberger2000physiobank,
  author  = {Goldberger, Ary L. and Amaral, Luis A. N. and Glass, Leon and
             Hausdorff, Jeffrey M. and Ivanov, Plamen Ch. and Mark, Roger G.
             and Mietus, Joseph E. and Moody, George B. and Peng, Chung-Kang
             and Stanley, H. Eugene},
  title   = {{PhysioBank, PhysioToolkit, and PhysioNet}: Components of a New
             Research Resource for Complex Physiologic Signals},
  journal = {Circulation},
  volume  = {101},
  number  = {23},
  pages   = {e215--e220},
  year    = {2000},
  doi     = {10.1161/01.CIR.101.23.e215}
}

@misc{eegmmidb2009,
  author       = {Schalk, Gerwin and McFarland, Dennis J. and Hinterberger,
                  Thilo and Birbaumer, Niels and Wolpaw, Jonathan R.},
  title        = {{EEG Motor Movement/Imagery Dataset}},
  howpublished = {PhysioNet},
  version      = {1.0.0},
  year         = {2009},
  doi          = {10.13026/C28G6P},
  url          = {https://physionet.org/content/eegmmidb/1.0.0/}
}

@article{gramfort2013mne,
  author  = {Gramfort, Alexandre and Luessi, Martin and Larson, Eric and
             Engemann, Denis A. and Strohmeier, Daniel and Brodbeck, Christian
             and Goj, Roman and Jas, Mainak and Brooks, Teon and Parkkonen,
             Lauri and H{\"a}m{\"a}l{\"a}inen, Matti S.},
  title   = {{MEG and EEG data analysis with MNE-Python}},
  journal = {Frontiers in Neuroscience},
  volume  = {7},
  pages   = {267},
  year    = {2013},
  doi     = {10.3389/fnins.2013.00267},
  url     = {https://mne.tools/}
}
```

---

## Plain-text references

- Schalk, G., McFarland, D. J., Hinterberger, T., Birbaumer, N., & Wolpaw, J. R.
  (2004). BCI2000: A General-Purpose Brain-Computer Interface (BCI) System.
  *IEEE Transactions on Biomedical Engineering, 51*(6), 1034–1043.
  https://doi.org/10.1109/TBME.2004.827072

- Goldberger, A. L., Amaral, L. A. N., Glass, L., Hausdorff, J. M., Ivanov,
  P. Ch., Mark, R. G., Mietus, J. E., Moody, G. B., Peng, C.-K., & Stanley,
  H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a New
  Research Resource for Complex Physiologic Signals. *Circulation, 101*(23),
  e215–e220. https://doi.org/10.1161/01.CIR.101.23.e215

- EEG Motor Movement/Imagery Dataset (version 1.0.0). PhysioNet (2009).
  https://doi.org/10.13026/C28G6P · https://physionet.org/content/eegmmidb/1.0.0/

- Gramfort, A., Luessi, M., Larson, E., Engemann, D. A., Strohmeier, D.,
  Brodbeck, C., Goj, R., Jas, M., Brooks, T., Parkkonen, L., & Hämäläinen, M. S.
  (2013). MEG and EEG data analysis with MNE-Python. *Frontiers in
  Neuroscience, 7*, 267. https://doi.org/10.3389/fnins.2013.00267 ·
  https://mne.tools/

---

## How to cite this repository

> *eeg-signal-processing-lab* (v1.0.0). A reproducible EEG signal-processing lab
> using the PhysioNet EEG Motor Movement/Imagery Dataset and MNE-Python.
> https://github.com/jevrton-code/eeg-signal-processing-lab

```bibtex
@software{eeg_signal_processing_lab,
  author  = {{eeg-signal-processing-lab contributors}},
  title   = {eeg-signal-processing-lab: A reproducible EEG signal-processing lab},
  version = {1.0.0},
  year    = {2026},
  url      = {https://github.com/jevrton-code/eeg-signal-processing-lab}
}
```

When citing this repository, please **also cite the dataset and MNE-Python**
above — this project is a wrapper around public data and open-source tooling.

---

## Licensing

These licenses are **independent** and must not be conflated:

| Component | License |
| --- | --- |
| **This repository's code** (the `eeg_lab` package, notebooks, reports, and documentation) | [MIT License](LICENSE) |
| **The EEG Motor Movement/Imagery Dataset** | Open Data Commons Attribution License v1.0 (ODC-By), via PhysioNet |

The MIT license covers only the code and documentation in this repository. It
grants **no rights** over the dataset. Use of the dataset is governed solely by
its ODC-By terms and requires attribution to PhysioNet and the dataset authors
as shown above. The dataset is **not redistributed** in this repository.
