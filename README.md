# Microstructure-Informed Fatigue Crack-Growth Prediction in Stainless Steel

This repository demonstrates a PhD-level computational workflow for fatigue crack-growth prediction in stainless steels using open/literature data, fracture-mechanics baselines, microstructure descriptors, and machine learning.

## Why this project exists

The project is designed for research applications in computational mechanics and materials modelling, especially topics involving:

- high-temperature structural integrity,
- fatigue crack growth,
- stainless steels and nickel-based structural alloys,
- microstructure-sensitive modelling,
- physics-guided machine learning,
- reproducible scientific programming.

The repository does **not** claim new laboratory measurements. It uses open/literature datasets and clearly labels which rows are measured and which are literature-reconstructed.

## Data sources

### 1. Open measured fatigue-crack-growth data

The primary measured data comes from the University of Southampton dataset:

> Cunningham et al., Dataset for *Fatigue crack initiation and growth behaviour in a notch with periodic overloads in the low cycle fatigue regime of FV566 ex-service steam turbine blade material*, DOI: `10.5258/SOTON/D2015`.

The downloaded workbook is stored at:

```text
data/raw/soton_D2015_FV566_fatigue_crack_growth.xlsx
```

The processed modelling table is stored at:

```text
data/processed/literature_open_crack_growth_dataset.csv
```

### 2. Literature-reconstructed austenitic stainless-steel reference curve

AISI 304L stainless steel reference data are reconstructed from reported Paris-law constants in Fan et al. (2008), *Modeling of fatigue crack growth of stainless steel 304L*, where the reported Paris parameters are used only to generate a labelled reference curve:

```text
C = 1.22e-10 m/cycle/(MPa√m)^m
m = 2.07
```

These rows are labelled as:

```text
data_type = literature_reconstructed
```

### 3. NIMS metadata references

The repository includes NIMS metadata references for SUS304 stainless-steel fatigue data sheets:

```text
data/raw/nims_reference_metadata.csv
```

The NIMS entries are included as traceable references, not as extracted numeric measurements. Direct NIMS Fatigue Data Sheet access may require service/account access depending on the data sheet portal.

## Scientific workflow

The repository implements:

1. extraction of fatigue crack-growth curves from open datasets,
2. Paris-law baseline fitting,
3. feature engineering for loading and microstructure descriptors,
4. machine-learning prediction of `log10(da/dN)`,
5. permutation-based feature importance,
6. research-quality plots and metrics.

## Repository structure

```text
.
├── data/
│   ├── raw/
│   │   ├── soton_D2015_FV566_fatigue_crack_growth.xlsx
│   │   └── nims_reference_metadata.csv
│   └── processed/
│       └── literature_open_crack_growth_dataset.csv
├── src/
│   ├── data.py
│   ├── features.py
│   ├── fracture_models.py
│   ├── train.py
│   └── plots.py
├── figures/
├── results/
├── reports/
│   └── technical_note.md
├── tests/
└── requirements.txt
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.train
python -m src.plots
pytest
```

## Current results

The current grouped test split gives:

- R² on log10 crack-growth rate: about `0.80`
- MAE on log10 crack-growth rate: about `0.22`

These values are not presented as a final research claim. They show that the workflow can learn meaningful structure from loading, material, condition, and microstructure-related features.

Generated figures include:

```text
figures/paris_fit_measured_fv566.png
figures/ml_predicted_vs_true.png
figures/feature_importance.png
```

## Why this is relevant to a PhD on high-temperature structural integrity

The project directly demonstrates transferable skills needed for microstructure-sensitive structural integrity research:

- fatigue crack-growth modelling,
- Paris-law and stress-intensity-factor reasoning,
- stainless-steel data handling,
- physics-guided feature engineering,
- microstructure descriptors such as hardness, grain-size proxy, microstructure family, and material class,
- machine-learning surrogate modelling,
- transparent reporting of data limitations.

## Limitations and honest scope

- The open measured data in this repository are from FV566 stainless steel, not from a newly generated lab campaign.
- The austenitic 304L rows are reconstructed from literature-reported Paris-law constants and are clearly labelled as such.
- NIMS entries are included as metadata references only.
- The project should be extended with digitised or tabulated SUS304/316L/Ni-base superalloy crack-growth data when available.

## Suggested future extensions

1. Add direct NIMS SUS304 crack-growth data if access/download is available.
2. Add 316L and nickel-base superalloy data from open supplementary files.
3. Add temperature-dependent creep-fatigue features.
4. Include crystal-plasticity or RVE-derived microstructure descriptors.
5. Replace proxy features with EBSD-derived grain-size/orientation/twin-boundary metrics.

## Citation

Please cite the original dataset and literature sources when using this repository.

## Added PhD-level extensions

This upgraded version also includes two extension modules that make the project closer to the LiU PhD topic.

### Extension 1: CrackPy / CrackMNIST-inspired DIC crack analysis

Folder:

```text
extensions/crackpy_crackmnist/
```

This module adds a DIC-style crack-tip analysis demonstration. It generates a synthetic full-field displacement map, estimates the crack-tip location from displacement-gradient concentration, and extracts DIC-inspired fracture features. The folder is intentionally written as an integration scaffold rather than a copy of external third-party repositories.

Run:

```bash
python extensions/crackpy_crackmnist/dic_crack_tip_demo.py
```

Outputs:

```text
extensions/crackpy_crackmnist/results/synthetic_dic_displacement_uy.png
extensions/crackpy_crackmnist/results/synthetic_dic_gradient_crack_tip.png
extensions/crackpy_crackmnist/results/dic_crack_tip_features.csv
```

### Extension 2: DAMASK / crystal-plasticity RVE-inspired microstructure module

Folder:

```text
extensions/damask_crystal_plasticity/
```

This module addresses the microstructure-modelling gap. It creates a synthetic Voronoi polycrystal, assigns grain orientations and strength heterogeneity, and extracts RVE-level descriptors such as orientation statistics, boundary fraction, and a strain-localization proxy. It is designed as a practical bridge toward DAMASK or Abaqus UMAT crystal-plasticity work.

Run:

```bash
python extensions/damask_crystal_plasticity/rve_microstructure_demo.py
```

Outputs:

```text
extensions/damask_crystal_plasticity/results/rve_grain_map.png
extensions/damask_crystal_plasticity/results/rve_orientation_map.png
extensions/damask_crystal_plasticity/results/rve_localization_proxy.png
extensions/damask_crystal_plasticity/results/rve_microstructure_features.csv
```

## Important note on third-party projects

This repository does not redistribute CrackPy, CrackMNIST, DAMASK, or Oxford Crystal Plasticity source code/data. The extension modules are original lightweight demonstrations and integration scaffolds. Future research versions can connect directly to those external packages following their respective licences and installation instructions.
