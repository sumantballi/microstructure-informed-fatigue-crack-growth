"""Synthetic DIC crack-tip feature extraction demo.

This script intentionally avoids redistributing external CrackMNIST/CrackPy data.
It creates a synthetic displacement field with a crack-tip-like singularity,
estimates the crack-tip location from displacement gradients, and exports
features that can be merged into fatigue crack-growth modelling workflows.
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_synthetic_dic_field(n: int = 128, crack_tip=(0.18, 0.0), seed: int = 7):
    rng = np.random.default_rng(seed)
    x = np.linspace(-1, 1, n)
    y = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(x, y)
    dx = X - crack_tip[0]
    dy = Y - crack_tip[1]
    r = np.sqrt(dx**2 + dy**2) + 1e-4
    theta = np.arctan2(dy, dx)

    # Crack-tip-like displacement fields. This is a simplified educational field,
    # not a replacement for real DIC or LEFM fitting.
    ux = 0.012 * np.sqrt(r) * np.cos(theta / 2) * (1 - np.sin(theta / 2) * np.sin(3 * theta / 2))
    uy = 0.018 * np.sqrt(r) * np.sin(theta / 2) * (2 + np.cos(theta / 2) * np.cos(3 * theta / 2))

    # Add a localized process-zone displacement concentration around the crack tip
    # so the educational crack-tip estimator has a clear DIC-like signal.
    process_zone = np.exp(-((dx / 0.055) ** 2 + (dy / 0.055) ** 2))
    ux += 0.006 * process_zone
    uy += 0.010 * process_zone

    # Add mild measurement noise similar to DIC uncertainty.
    ux += rng.normal(0, 0.00035, ux.shape)
    uy += rng.normal(0, 0.00035, uy.shape)
    return X, Y, ux, uy


def estimate_crack_tip(X, Y, ux, uy):
    dux_dy, dux_dx = np.gradient(ux, Y[:, 0], X[0, :])
    duy_dy, duy_dx = np.gradient(uy, Y[:, 0], X[0, :])
    grad_mag = np.sqrt(dux_dx**2 + dux_dy**2 + duy_dx**2 + duy_dy**2)

    # Avoid noisy boundaries and the idealized crack wake. In real DIC workflows,
    # the search region would be constrained by the visible crack path or by a
    # segmentation model. Here we keep the search in the expected process zone
    # ahead of the synthetic crack.
    search_mask = (X > 0.12) & (X < 0.55) & (Y > -0.45) & (Y < 0.45)
    masked = np.where(search_mask, grad_mag, -np.inf)
    iy, ix = np.unravel_index(np.argmax(masked), masked.shape)
    return float(X[iy, ix]), float(Y[iy, ix]), grad_mag


def extract_features(X, Y, ux, uy, tip_x, tip_y, grad_mag):
    r = np.sqrt((X - tip_x) ** 2 + (Y - tip_y) ** 2)
    near = (r > 0.04) & (r < 0.20)
    far = (r >= 0.20) & (r < 0.55)
    return {
        "estimated_tip_x": tip_x,
        "estimated_tip_y": tip_y,
        "mean_near_tip_gradient": float(np.mean(grad_mag[near])),
        "p95_near_tip_gradient": float(np.percentile(grad_mag[near], 95)),
        "mean_far_field_gradient": float(np.mean(grad_mag[far])),
        "dic_gradient_concentration_ratio": float(np.mean(grad_mag[near]) / (np.mean(grad_mag[far]) + 1e-12)),
    }


def save_plots(out_dir: Path, X, Y, ux, uy, grad_mag, tip_x, tip_y):
    out_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(6, 5))
    plt.contourf(X, Y, uy, levels=40)
    plt.scatter([tip_x], [tip_y], marker="x", s=80)
    plt.title("Synthetic DIC vertical displacement with estimated crack tip")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.colorbar(label="u_y")
    plt.tight_layout()
    plt.savefig(out_dir / "synthetic_dic_displacement_uy.png", dpi=180)
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.contourf(X, Y, grad_mag, levels=40)
    plt.scatter([tip_x], [tip_y], marker="x", s=80)
    plt.title("Displacement-gradient magnitude used for crack-tip estimate")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.colorbar(label="gradient magnitude")
    plt.tight_layout()
    plt.savefig(out_dir / "synthetic_dic_gradient_crack_tip.png", dpi=180)
    plt.close()


def main():
    out_dir = Path(__file__).resolve().parent / "results"
    X, Y, ux, uy = generate_synthetic_dic_field()
    tip_x, tip_y, grad_mag = estimate_crack_tip(X, Y, ux, uy)
    features = extract_features(X, Y, ux, uy, tip_x, tip_y, grad_mag)
    save_plots(out_dir, X, Y, ux, uy, grad_mag, tip_x, tip_y)
    pd.DataFrame([features]).to_csv(out_dir / "dic_crack_tip_features.csv", index=False)
    print("Saved DIC demo outputs to", out_dir)
    print(features)


if __name__ == "__main__":
    main()
