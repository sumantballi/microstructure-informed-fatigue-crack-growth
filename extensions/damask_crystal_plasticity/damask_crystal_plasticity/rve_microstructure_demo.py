"""Synthetic polycrystal RVE feature demo.

This script provides a microstructure-modelling extension for the fatigue
crack-growth repository. It generates a 2D Voronoi polycrystal and computes
simple microstructure descriptors and a strain-localization proxy.

The purpose is to demonstrate the modelling pathway. For a full research study,
replace the proxy with DAMASK or Abaqus UMAT crystal-plasticity outputs.
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree


def generate_voronoi_microstructure(n_grid: int = 160, n_grains: int = 45, seed: int = 11):
    rng = np.random.default_rng(seed)
    points = rng.random((n_grains, 2))
    x = np.linspace(0, 1, n_grid)
    y = np.linspace(0, 1, n_grid)
    X, Y = np.meshgrid(x, y)
    grid_points = np.column_stack([X.ravel(), Y.ravel()])
    tree = cKDTree(points)
    _, grain_ids = tree.query(grid_points)
    grain_map = grain_ids.reshape(n_grid, n_grid)
    return X, Y, points, grain_map


def assign_grain_properties(n_grains: int, seed: int = 11):
    rng = np.random.default_rng(seed)
    orientation_deg = rng.uniform(0, 180, n_grains)
    grain_strength = rng.normal(1.0, 0.08, n_grains)  # dimensionless strength proxy
    return orientation_deg, grain_strength


def compute_localization_proxy(grain_map, orientation_deg, grain_strength):
    theta = np.deg2rad(orientation_deg)
    # Schmid-like orientation sensitivity proxy under uniaxial loading.
    orientation_factor = np.abs(np.sin(2 * theta))
    grain_response = orientation_factor / grain_strength
    response_map = grain_response[grain_map]

    # Add grain-boundary amplification because incompatibility often localizes near boundaries.
    boundary = np.zeros_like(grain_map, dtype=bool)
    boundary[:, 1:] |= grain_map[:, 1:] != grain_map[:, :-1]
    boundary[1:, :] |= grain_map[1:, :] != grain_map[:-1, :]
    localization_map = response_map * (1.0 + 0.35 * boundary.astype(float))
    localization_map /= np.mean(localization_map)
    return localization_map, boundary


def extract_rve_features(grain_map, orientation_deg, localization_map, boundary):
    unique, counts = np.unique(grain_map, return_counts=True)
    area_fracs = counts / counts.sum()
    return {
        "n_grains": int(len(unique)),
        "mean_grain_area_fraction": float(np.mean(area_fracs)),
        "std_grain_area_fraction": float(np.std(area_fracs)),
        "mean_orientation_deg": float(np.mean(orientation_deg)),
        "std_orientation_deg": float(np.std(orientation_deg)),
        "localization_index_p95_over_mean": float(np.percentile(localization_map, 95) / np.mean(localization_map)),
        "max_localization_over_mean": float(np.max(localization_map) / np.mean(localization_map)),
        "boundary_pixel_fraction": float(np.mean(boundary)),
    }


def save_figures(out_dir: Path, grain_map, orientation_deg, localization_map, boundary):
    out_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(5.5, 5))
    plt.imshow(grain_map, origin="lower")
    plt.title("Synthetic Voronoi polycrystal grain map")
    plt.axis("off")
    plt.colorbar(label="grain ID")
    plt.tight_layout()
    plt.savefig(out_dir / "rve_grain_map.png", dpi=180)
    plt.close()

    orientation_map = orientation_deg[grain_map]
    plt.figure(figsize=(5.5, 5))
    plt.imshow(orientation_map, origin="lower")
    plt.title("Assigned grain orientation map")
    plt.axis("off")
    plt.colorbar(label="orientation [deg]")
    plt.tight_layout()
    plt.savefig(out_dir / "rve_orientation_map.png", dpi=180)
    plt.close()

    plt.figure(figsize=(5.5, 5))
    plt.imshow(localization_map, origin="lower")
    plt.title("Simplified strain-localization proxy")
    plt.axis("off")
    plt.colorbar(label="relative localization")
    plt.tight_layout()
    plt.savefig(out_dir / "rve_localization_proxy.png", dpi=180)
    plt.close()


def main():
    out_dir = Path(__file__).resolve().parent / "results"
    X, Y, points, grain_map = generate_voronoi_microstructure()
    orientation_deg, grain_strength = assign_grain_properties(points.shape[0])
    localization_map, boundary = compute_localization_proxy(grain_map, orientation_deg, grain_strength)
    features = extract_rve_features(grain_map, orientation_deg, localization_map, boundary)
    save_figures(out_dir, grain_map, orientation_deg, localization_map, boundary)
    pd.DataFrame([features]).to_csv(out_dir / "rve_microstructure_features.csv", index=False)
    print("Saved RVE demo outputs to", out_dir)
    print(features)


if __name__ == "__main__":
    main()
