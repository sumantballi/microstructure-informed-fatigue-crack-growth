from extensions.crackpy_crackmnist.dic_crack_tip_demo import generate_synthetic_dic_field, estimate_crack_tip, extract_features
from extensions.damask_crystal_plasticity.rve_microstructure_demo import generate_voronoi_microstructure, assign_grain_properties, compute_localization_proxy, extract_rve_features


def test_dic_feature_extraction_runs():
    X, Y, ux, uy = generate_synthetic_dic_field(n=48)
    tip_x, tip_y, grad = estimate_crack_tip(X, Y, ux, uy)
    features = extract_features(X, Y, ux, uy, tip_x, tip_y, grad)
    assert "dic_gradient_concentration_ratio" in features
    assert features["dic_gradient_concentration_ratio"] > 0


def test_rve_feature_extraction_runs():
    _, _, points, grain_map = generate_voronoi_microstructure(n_grid=48, n_grains=12)
    orientation, strength = assign_grain_properties(points.shape[0])
    localization, boundary = compute_localization_proxy(grain_map, orientation, strength)
    features = extract_rve_features(grain_map, orientation, localization, boundary)
    assert features["n_grains"] <= 12
    assert features["localization_index_p95_over_mean"] > 0
