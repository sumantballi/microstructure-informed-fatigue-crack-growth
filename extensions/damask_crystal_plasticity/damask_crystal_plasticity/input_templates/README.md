# DAMASK-style input template notes

This folder is intentionally lightweight. It documents where future DAMASK files would be placed:

- `material.yaml`: phase, homogenization and crystal-plasticity parameters.
- `grid.vti` or `grid.txt`: voxelized RVE / EBSD-derived microstructure.
- `load.yaml`: tension, cyclic loading, creep-fatigue or thermal loading definition.

The current repository includes a Python RVE proxy so the project can run without installing DAMASK. A full extension would replace this proxy with actual DAMASK simulation outputs.
