# Extension 2: DAMASK / crystal-plasticity RVE-inspired module

This extension addresses the main weakness of a purely tabular fatigue project: limited microstructure modelling.

## Purpose

The goal is to show a microstructure-sensitive modelling pathway using a representative volume element (RVE) concept. The current implementation is a lightweight Python demonstrator that creates a synthetic polycrystal, assigns grain orientations and strength heterogeneity, and computes a simplified strain-localization proxy.

It is **not** a replacement for a full DAMASK or Abaqus crystal-plasticity simulation. It is a repository-ready scaffold that can later be connected to DAMASK or an Abaqus UMAT.

## What is included

1. Synthetic 2D polycrystal generation using Voronoi tessellation.
2. Grain-level orientation and strength assignment.
3. Microstructure descriptors: grain area fraction, orientation statistics, localization index.
4. Visual maps for grain IDs, orientation, and strain-localization proxy.
5. Template files showing how a DAMASK-style material/grid workflow could be organized.

## Why this matters for the PhD

The LiU PhD project focuses on microstructural influence on deformation and crack-growth behaviour. This module demonstrates that the applicant understands how grain-scale structure can be converted into computational features for structural-integrity modelling.

## How to run

From the repository root:

```bash
python extensions/damask_crystal_plasticity/rve_microstructure_demo.py
```

Outputs are written to:

```text
extensions/damask_crystal_plasticity/results/
```

## Future work

- Replace the simplified localization proxy with a real DAMASK crystal-plasticity simulation.
- Add temperature-dependent viscoplasticity and creep-fatigue loading.
- Couple grain-boundary localization metrics with crack-initiation probability.
- Use EBSD data instead of synthetic Voronoi microstructures.
