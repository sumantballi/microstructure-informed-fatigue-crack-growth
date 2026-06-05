import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from .data import load_dataset, ROOT
from .features import NUMERIC_FEATURES, CATEGORICAL_FEATURES, build_X_y


def make_pipeline(model='hgb'):
    pre = ColumnTransformer([
        ('num', StandardScaler(), NUMERIC_FEATURES),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES),
    ])
    reg = GradientBoostingRegressor(n_estimators=180, learning_rate=0.05, max_depth=3, random_state=42) if model == 'hgb' else RandomForestRegressor(n_estimators=120, min_samples_leaf=3, random_state=42, n_jobs=-1)
    return Pipeline([('preprocess', pre), ('model', reg)])


def train_and_evaluate():
    df = load_dataset()
    X, y = build_X_y(df)
    # split by source+condition to reduce leakage between closely related curves
    groups = df['source_dataset'].astype(str) + '_' + df['condition'].astype(str) + '_' + df['loading_protocol'].astype(str)
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=7)
    train_idx, test_idx = next(splitter.split(X, y, groups))
    X_train, X_test, y_train, y_test = X.iloc[train_idx], X.iloc[test_idx], y.iloc[train_idx], y.iloc[test_idx]
    pipe = make_pipeline('hgb')
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    metrics = {
        'target': 'log10(da/dN in mm/cycle)',
        'n_rows_total': int(len(df)),
        'n_train': int(len(train_idx)),
        'n_test': int(len(test_idx)),
        'r2_log_target': float(r2_score(y_test, pred)),
        'mae_log10': float(mean_absolute_error(y_test, pred)),
        'rmse_log10': float(mean_squared_error(y_test, pred) ** 0.5),
        'notes': 'Dataset combines measured open Southampton D2015 fatigue-crack-growth data and a clearly labelled 304L literature-reconstructed Paris curve.'
    }
    out = ROOT / 'results'
    out.mkdir(exist_ok=True)
    pd.DataFrame({'y_true_log_dadn': y_test, 'y_pred_log_dadn': pred, 'row_index': y_test.index}).merge(
        df.reset_index().rename(columns={'index':'row_index'}), on='row_index', how='left'
    ).to_csv(out / 'test_predictions.csv', index=False)
    with open(out / 'metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    # permutation importance on sample
    sample_n = min(120, len(X_test))
    imp = permutation_importance(pipe, X_test.iloc[:sample_n], y_test.iloc[:sample_n], n_repeats=3, random_state=42, scoring='r2')
    feature_names = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    pd.DataFrame({'feature': feature_names, 'importance_mean': imp.importances_mean[:len(feature_names)], 'importance_std': imp.importances_std[:len(feature_names)]}).sort_values('importance_mean', ascending=False).to_csv(out / 'permutation_importance.csv', index=False)
    return metrics

if __name__ == '__main__':
    print(json.dumps(train_and_evaluate(), indent=2))
