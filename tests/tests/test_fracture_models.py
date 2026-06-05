import numpy as np
from src.fracture_models import paris_law, fit_paris_law


def test_paris_law_monotonic():
    dk = np.array([5, 10, 20])
    y = paris_law(dk, 1e-8, 3)
    assert np.all(np.diff(y) > 0)


def test_fit_paris_law_recovers_slope():
    dk = np.linspace(5, 30, 20)
    dadn = paris_law(dk, 2e-9, 2.5)
    C, m, _ = fit_paris_law(dk, dadn)
    assert abs(m - 2.5) < 1e-8
    assert abs(C - 2e-9) < 1e-16
