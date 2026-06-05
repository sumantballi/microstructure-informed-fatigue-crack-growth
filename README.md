# Microstructure-Informed Fatigue Crack-Growth Prediction in Stainless Steel

## Project Summary

This project develops a microstructure-informed framework for fatigue crack-growth prediction in austenitic stainless steel. Open/literature fatigue crack-growth datasets are combined with fracture-mechanics descriptors, microstructure-sensitive features, and machine-learning models to predict crack-growth rates.

### Key Contributions

- Physics-based Paris/Walker crack-growth modelling
- Machine-learning prediction of fatigue crack-growth rate
- Microstructure-sensitive feature engineering
- DIC-inspired crack-tip analysis extension
- Crystal-plasticity/RVE-inspired microstructure modelling extension
- Reproducible Python workflow with uncertainty analysis

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

1. Extraction of fatigue crack-growth curves from open datasets,
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


