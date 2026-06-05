from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from .data import load_dataset, ROOT
from .fracture_models import fit_paris_law, paris_law

FIG = ROOT / 'figures'
RES = ROOT / 'results'

def plot_paris_fit():
    df = load_dataset()
    subset = df[(df['alloy'].eq('FV566 stainless steel')) & (df['data_type'].eq('measured')) & (df['dadn_mm_per_cycle']>0)]
    C, m, _ = fit_paris_law(subset['delta_k_mpa_sqrt_m'], subset['dadn_mm_per_cycle'])
    x = np.linspace(subset['delta_k_mpa_sqrt_m'].min(), subset['delta_k_mpa_sqrt_m'].max(), 200)
    y = paris_law(x, C, m)
    plt.figure(figsize=(7,5))
    for cond, g in subset.groupby('condition'):
        plt.scatter(g['delta_k_mpa_sqrt_m'], g['dadn_mm_per_cycle'], s=16, alpha=0.55, label=cond)
    plt.plot(x, y, linewidth=2, label=f'Paris fit: C={C:.2e}, m={m:.2f}')
    plt.xscale('log'); plt.yscale('log')
    plt.xlabel(r'$\Delta K$ [MPa$\sqrt{m}$]')
    plt.ylabel(r'$da/dN$ [mm/cycle]')
    plt.title('Measured open-data fatigue crack growth: FV566 stainless steel')
    plt.legend(fontsize=8)
    plt.tight_layout(); plt.savefig(FIG / 'paris_fit_measured_fv566.png', dpi=220); plt.close()


def plot_ml_predictions():
    pred_path = RES / 'test_predictions.csv'
    if not pred_path.exists():
        raise FileNotFoundError('Run python -m src.train first.')
    df = pd.read_csv(pred_path)
    plt.figure(figsize=(6,5))
    plt.scatter(df['y_true_log_dadn'], df['y_pred_log_dadn'], s=18, alpha=0.65)
    lims = [min(df['y_true_log_dadn'].min(), df['y_pred_log_dadn'].min()), max(df['y_true_log_dadn'].max(), df['y_pred_log_dadn'].max())]
    plt.plot(lims, lims, linestyle='--')
    plt.xlabel('True log10(da/dN)')
    plt.ylabel('Predicted log10(da/dN)')
    plt.title(f'ML prediction on held-out groups; R²={r2_score(df["y_true_log_dadn"], df["y_pred_log_dadn"]):.3f}')
    plt.tight_layout(); plt.savefig(FIG / 'ml_predicted_vs_true.png', dpi=220); plt.close()


def plot_feature_importance():
    imp_path = RES / 'permutation_importance.csv'
    if not imp_path.exists():
        raise FileNotFoundError('Run python -m src.train first.')
    imp = pd.read_csv(imp_path).sort_values('importance_mean').tail(10)
    plt.figure(figsize=(7,5))
    plt.barh(imp['feature'], imp['importance_mean'])
    plt.xlabel('Permutation importance (R² drop)')
    plt.title('Microstructure/loading feature importance')
    plt.tight_layout(); plt.savefig(FIG / 'feature_importance.png', dpi=220); plt.close()


def plot_all():
    FIG.mkdir(exist_ok=True)
    plot_paris_fit(); plot_ml_predictions(); plot_feature_importance()

if __name__ == '__main__':
    plot_all()
