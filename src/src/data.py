from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'data' / 'processed' / 'literature_open_crack_growth_dataset.csv'

def load_dataset(path=DATASET):
    df = pd.read_csv(path)
    required = {'delta_k_mpa_sqrt_m', 'dadn_mm_per_cycle', 'log_delta_k', 'log_dadn'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing columns: {missing}')
    return df
