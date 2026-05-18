#!/usr/bin/env python3
import numpy as np

def bootstrap_mean_ci(values, n_boot=10000, seed=13, alpha=0.05):
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(values), size=(n_boot, len(values)))
    means = values[idx].mean(axis=1)
    return float(values.mean()), float(np.quantile(means, alpha/2)), float(np.quantile(means, 1-alpha/2))
