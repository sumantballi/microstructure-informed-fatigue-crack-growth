import pandas as pd

NUMERIC_FEATURES = [
    'log_delta_k', 'delta_k_mpa_sqrt_m', 'overload_ratio', 'hardness_hv',
    'temperature_C', 'stress_ratio_R', 'grain_size_um_filled',
    'inv_sqrt_grain_size', 'is_austenitic', 'is_measured'
]
CATEGORICAL_FEATURES = ['condition', 'loading_protocol', 'microstructure_family', 'material_class']

def build_X_y(df: pd.DataFrame):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    X['stress_ratio_R'] = X['stress_ratio_R'].fillna(-999.0)
    y = df['log_dadn'].copy()
    return X, y
