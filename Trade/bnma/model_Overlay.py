#!/usr/bin/env python3
"""PyMC model for Overlay group BNMA"""
import numpy as np
import pymc as pm
import arviz as az

# Data arrays (populated from stage_a.csv)
y_obs = np.array([...])      # observed Sharpe ratios
se_obs = np.array([...])     # study SEs
var_idx = np.array([...])    # variable index per observation
ac_idx = np.array([...])     # asset-class index per observation
prior_sds = np.array([...])  # grade-tiered prior SDs per variable

n_vars = 3
n_acs = ...  # number of unique asset classes
tau_prior_sd = 0.15

with pm.Model() as model:
    # Grade-tiered priors via non-centered parameterization
    mu_k_raw = pm.Normal("mu_k_raw", mu=0, sigma=1, shape=n_vars)
    mu_k = pm.Deterministic("mu_k", mu_k_raw * prior_sds)

    # Asset-class intercept
    alpha_a = pm.Normal("alpha_a", mu=0, sigma=0.3, shape=n_acs)

    # Per-variable heterogeneity
    tau_k = pm.HalfNormal("tau_k", sigma=tau_prior_sd, shape=n_vars)

    # Study-level random effects (non-centered)
    theta_raw = pm.Normal("theta_raw", mu=0, sigma=1, shape=len(y_obs))
    theta = pm.Deterministic("theta", mu_k[var_idx] + alpha_a[ac_idx] + tau_k[var_idx] * theta_raw)

    # Likelihood
    y = pm.Normal("y", mu=theta, sigma=se_obs, observed=y_obs)

    # NUTS sampling
    trace = pm.sample(2000, tune=2000, chains=4, cores=4,
                      random_seed=42, return_inferencedata=True)

# Convergence diagnostics
summary = az.summary(trace, var_names=["mu_k", "alpha_a", "tau_k"])
assert summary["r_hat"].max() < 1.01, "R-hat convergence failure"
assert summary["ess_bulk"].min() > 400, "ESS too low"

trace.to_netcdf("trace_Overlay.nc")
print(summary)
