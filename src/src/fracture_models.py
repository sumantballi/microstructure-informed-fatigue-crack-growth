import numpy as np

def paris_law(delta_k, C, m):
    """Paris law: da/dN = C * (Delta K)^m."""
    delta_k = np.asarray(delta_k, dtype=float)
    return C * np.power(delta_k, m)

def fit_paris_law(delta_k, dadn):
    """Fit Paris law in log10 space and return C, m, and fitted log values."""
    delta_k = np.asarray(delta_k, dtype=float)
    dadn = np.asarray(dadn, dtype=float)
    mask = (delta_k > 0) & (dadn > 0)
    x = np.log10(delta_k[mask])
    y = np.log10(dadn[mask])
    m, logC = np.polyfit(x, y, 1)
    return 10 ** logC, m, logC + m * x

def walker_effective_delta_k(delta_k, stress_ratio_R, gamma=0.5):
    """Walker correction: DeltaK_eff = DeltaK / (1-R)^(1-gamma)."""
    r = np.asarray(stress_ratio_R, dtype=float)
    return np.asarray(delta_k, dtype=float) / np.power(1 - r, 1 - gamma)
