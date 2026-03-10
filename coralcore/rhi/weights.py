# 🪸 RHI Weights - Pure Python
PCA_WEIGHTS = {
    'g_ca': 0.19,
    'e_diss': 0.14,
    'phi_ps': 0.21,
    'rho_skel': 0.12,
    'delta_ph': 0.11,
    's_reef': 0.10,
    'k_s': 0.08,
    't_thr': 0.05
}

def load_weights(config='pca_default'):
    return PCA_WEIGHTS.copy()
