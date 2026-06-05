# Extension 1: CrackPy / CrackMNIST-inspired DIC crack-growth module

This extension strengthens the main repository by adding a fracture-mechanics imaging workflow inspired by the open DLR CrackPy/CrackMNIST ecosystem.

## Purpose

The main project predicts fatigue crack-growth rate from tabular literature data. This extension shows how the same research direction can be connected to full-field Digital Image Correlation (DIC) displacement data, crack-tip localization, and stress-intensity-factor estimation.

## What is included here

This folder does **not** vendor or redistribute the external CrackPy or CrackMNIST repositories. Instead, it contains a lightweight, reproducible demonstration that:

1. Generates a synthetic DIC-like displacement field around a fatigue crack tip.
2. Estimates the crack-tip location from the displacement-gradient magnitude.
3. Extracts simplified fracture features that can be merged with the tabular crack-growth dataset.
4. Saves visual outputs and a feature table for downstream modelling.

## Why this matters for the PhD

The LiU PhD project involves advanced modelling of deformation, crack growth, and structural integrity. DIC-based crack-tip analysis is a natural experimental/computational bridge, because it links measured displacement fields to fracture-mechanics quantities.

## How to run

From the repository root:

```bash
python extensions/crackpy_crackmnist/dic_crack_tip_demo.py
```

Outputs are written to:

```text
extensions/crackpy_crackmnist/results/
```

## Future work

- Replace the synthetic displacement field with real CrackMNIST DIC fields.
- Use CrackPy for proper Williams-series fitting, stress-intensity factors, and J-integral analysis.
- Train a CNN model for crack-tip or SIF prediction from DIC maps.
