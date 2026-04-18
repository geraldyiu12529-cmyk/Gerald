"""
Plackett-Luce Bayesian Network Meta-Analysis (PL-BNMA)
======================================================
Full all-vs-all comparison across 12 papers covering Gerald's trading framework:

  - 4 BNMA runs (P1 = BNMA Mark 1; P2 = Chatgpt Mark 1; P3 = Chatgpt mark 2; P4 = bnma-claude mark 2)
  - 8 AI systematic reviews (cg1–cg5, cl1–cl3) covering new candidate variables

Methodology
-----------
The user asked for an all-vs-all ranking WITHOUT group (S/T/R/Overlay) structure.
The BNMA papers themselves warn that cross-group posterior medians are NOT on a
common Sharpe scale (S/T = long-short Sharpe; R = risk-sizing Sharpe improvement;
Overlay = conditional Sharpe gain). A naive raw-posterior meta-regression would
conflate these.

The rigorous route: a Plackett-Luce ranking model that uses only the WITHIN-PAPER
ORDINAL information (which variable ranks higher than which, within a paper).
The per-variable latent strength θ is scale-free. This is the standard solution
in ranking-aggregation / sports-like meta-analysis (Guiver-Snelson 2009, Caron-
Teh 2012).

We reduce each ranking to pairwise comparisons (equivalent to Plackett-Luce in
the softmax utility limit). The Bradley-Terry pairwise likelihood is:

    P(i beats j) = σ(θ_i − θ_j)

Priors:
    θ_i ~ Normal(0, σ²_θ)  with σ_θ = 1.0 (weakly informative)
    θ_ref = 0              (V009 TSMOM fixed at 0 for identifiability)

Inference: MAP + Laplace approximation (normal posterior around MAP), then
sample 10,000 draws from the Laplace approximation to compute:
  - Posterior mean θ per variable
  - 95% credible interval
  - Rank distribution (probability of being ranked k-th)
  - All-vs-all pairwise dominance matrix P(θ_i > θ_j)

Scale caveat
------------
Cross-group within-paper comparisons (e.g., V028 S-group = 0.79 vs V027 R-group
= 0.81 in P1) rely on the implicit assumption that "higher posterior median in
paper p" ⇒ "higher tradable quality" regardless of the group's Sharpe
construct. This is stronger than the within-group assumption used in the
original BNMA runs. The report labels this explicitly and presents a
within-group sensitivity check for comparison.
"""

import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit  # numerically stable sigmoid

rng = np.random.default_rng(20260418)

# =============================================================================
# 1. Per-paper rankings
# =============================================================================
# Each paper contributes a within-paper ordering over the subset of variables
# it covers. We encode as a dict var_id -> rank_score (higher = better).
# We then sort within paper to produce a ranking.
#
# For BNMA papers: rank_score = posterior_median. Approx-0 entries (analytical
# shrinkage artifacts from P2/P3) are excluded — they are NOT evidence of zero.
# Overlay C-series IDs vary across papers; we use paper-specific suffixes so
# the network doesn't spuriously merge unrelated constructs.

# BNMA input values = p_beats_peers (joint-posterior peer-dominance probability,
# i.e. probability that this variable's effect exceeds a randomly chosen peer
# within its within-paper posterior). This is the ordinal metric the original
# BNMA authors used for their DEPLOY verdicts. Extracted from the consolidated
# table in `BNMA-meta-analysis-2026-04-18.md` (cell format:
# `(post_median, p_positive, p_beats_peers, flags)`).
#
# Entries marked "approx0" in P2/P3 are OMITTED — they are prior-shrinkage
# artifacts with uninformative symmetric CI and no genuine likelihood evidence.
# Their p_beats_peers ≈ 0.50 is a prior artifact, not data.

P1 = {  # BNMA Mark 1 — full MCMC
    # S-group
    "V003": 0.05, "V006": 0.37, "V007": 0.30, "V008": 0.34, "V011": 0.49,
    "V012": 0.40, "V013": 0.35, "V019": 0.26, "V028": 0.51,
    # T-group
    "V009": 0.66, "V010": 0.10, "V014": 0.53, "V017": 0.04, "V026": 0.17,
    # R-group
    "V001": 0.81, "V002": 0.10, "V004": 0.62, "V005": 0.03, "V015": 0.01,
    "V016": 0.50, "V018": 0.50, "V027": 0.37,
    # Overlay
    "C009_FaberTAA": 0.68, "C011_VIXTermStructure": 0.32,
}

P2 = {  # Chatgpt Mark 1 — analytical; only non-approx0 entries.
    "V011": 0.19, "V028": 0.81,
    "V009": 0.99, "V026": 0.01,
    "V018": 0.81, "V027": 1.00,
}

P3 = {  # Chatgpt mark 2 — analytical; only non-approx0 entries.
    "V011": 0.19, "V028": 0.81,
    "V009": 0.99, "V026": 0.01,
    "V027": 1.00,
}

P4 = {  # bnma-claude mark 2 — full MCMC
    # S-group
    "V003": 0.43, "V006": 0.32, "V007": 0.35, "V008": 0.26, "V011": 0.50,
    "V012": 0.40, "V013": 0.40, "V019": 0.45, "V028": 0.50,
    # T-group
    "V009": 0.95, "V010": 0.01, "V014": 0.58, "V017": 0.42, "V026": 0.05,
    # R-group
    "V001": 0.24, "V002": 0.27, "V004": 0.05, "V005": 0.31, "V015": 0.64,
    "V016": 0.45, "V018": 0.55, "V027": 0.95,
    # Overlay
    "C005_200DMA": 0.40, "C002_VIXTermSlope": 0.38, "C007_MarketBreadth": 0.22,
}

BNMA_PAPERS = {"P1": P1, "P2": P2, "P3": P3, "P4": P4}

# =============================================================================
# 2. Systematic-review rankings — imported from the existing meta_analysis.py
# =============================================================================
# We convert each reviewer's per-variable grade+class+Sharpe into a rank-score:
#   score = grade_numeric
#         + 0.5 if class=EFFECTIVE, −0.5 if class=INEFFECTIVE, 0 if MIXED
#         + 0.3 × sharpe (if sharpe reported)
# Higher score = better. Ties broken by this composite (which gives the
# reviewer's ordinal preference over variables they reviewed).

GRADE_MAP = {"A": 3.0, "A-": 2.7, "B+": 2.3, "B": 2.0, "B-": 1.7,
             "B/C": 1.5, "C+": 1.3, "C": 1.0, "C-": 0.7,
             "PARTIAL": 0.5, "EXCLUDE": 0.0, "INCLUDE_UNGRADED": 1.8}

def review_score(entry):
    g = GRADE_MAP.get(entry["grade"], 0.0)
    cls_adj = {"EFFECTIVE": 0.5, "INEFFECTIVE": -0.5, "MIXED": 0.0}.get(entry["class"], 0.0)
    sh = entry.get("sharpe")
    sh_adj = 0.3 * sh if sh is not None else 0.0
    return g + cls_adj + sh_adj

# Load the review data from meta_analysis.py (by exec'ing just the VARIABLES dict).
META_PATH = Path("/sessions/sharp-sweet-euler/mnt/Bayesian Meta-Analysis/meta_analysis.py")
src = META_PATH.read_text(encoding="utf-8")
start = src.find("VARIABLES = {")
end = src.find("\n}\n\n", start) + 2
ns = {}
exec(src[start:end], ns)
REVIEW_VARIABLES = ns["VARIABLES"]

# Build per-reviewer rankings: reviewer -> {var_id -> score}
REVIEWER_RANKINGS = {rev: {} for rev in
                     ["cg1", "cg2", "cg3", "cg4", "cg5", "cl1", "cl2", "cl3"]}
for vid, v in REVIEW_VARIABLES.items():
    for rev, entry in v["reviews"].items():
        REVIEWER_RANKINGS[rev][vid] = review_score(entry)

# Drop empty reviewers (safety)
REVIEWER_RANKINGS = {r: d for r, d in REVIEWER_RANKINGS.items() if d}

# =============================================================================
# 3. Consolidated paper × variable ranking table
# =============================================================================
ALL_PAPERS = {**BNMA_PAPERS, **REVIEWER_RANKINGS}

# Unique variable universe (union across all papers)
ALL_VARS = sorted({v for paper in ALL_PAPERS.values() for v in paper})
VAR_INDEX = {v: i for i, v in enumerate(ALL_VARS)}
N_VARS = len(ALL_VARS)

print(f"Papers: {len(ALL_PAPERS)}  | Unique variables: {N_VARS}")
for p, d in ALL_PAPERS.items():
    print(f"  {p:5s} covers {len(d):>3} vars")

# =============================================================================
# 4. Reduce to pairwise comparisons
# =============================================================================
# For each paper, sort variables by rank-score (descending = best first).
# For each ordered pair (i above j) in the ranking, emit a pairwise "i beats j"
# observation. Ties are skipped (no comparison).
# Papers with only 1 variable contribute no comparisons.

pairs = []  # (winner_idx, loser_idx, paper_id)
for paper, scores in ALL_PAPERS.items():
    items = sorted(scores.items(), key=lambda kv: -kv[1])
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            v_i, s_i = items[i]
            v_j, s_j = items[j]
            if s_i > s_j:
                pairs.append((VAR_INDEX[v_i], VAR_INDEX[v_j], paper))
            # ties (s_i == s_j) → no comparison
print(f"Total pairwise comparisons: {len(pairs)}")

# =============================================================================
# 5. Bayesian Bradley-Terry fit (Laplace approximation)
# =============================================================================
# Negative log-posterior:
#   NLP(θ) = Σ log(1 + exp(−(θ_w − θ_l)))    [likelihood, logistic]
#          + 0.5 × Σ θ_i² / σ²_θ               [prior, Normal(0, σ²_θ)]
# with θ[ref_idx] fixed at 0 for identifiability.

SIGMA_PRIOR = 1.0
# Identifiability: the Normal(0, σ²_θ) prior on every θ_i pins the posterior
# (the likelihood is translation-invariant in θ, but the prior breaks that
# symmetry by pulling every θ toward 0). No fixed reference variable —
# every variable competes symmetrically.

w_idx = np.array([p[0] for p in pairs])
l_idx = np.array([p[1] for p in pairs])

def neg_log_posterior(theta):
    diff = theta[w_idx] - theta[l_idx]
    log_lik = np.logaddexp(0.0, -diff).sum()          # Σ softplus(-diff)
    log_prior = 0.5 * np.sum(theta**2) / (SIGMA_PRIOR**2)
    return log_lik + log_prior

def grad_neg_log_posterior(theta):
    diff = theta[w_idx] - theta[l_idx]
    p = expit(-diff)
    grad = np.zeros(N_VARS)
    np.add.at(grad, w_idx, -p)
    np.add.at(grad, l_idx,  p)
    grad += theta / (SIGMA_PRIOR**2)
    return grad

def hessian_neg_log_posterior(theta):
    diff = theta[w_idx] - theta[l_idx]
    p = expit(diff)
    w = p * (1.0 - p)
    H = np.zeros((N_VARS, N_VARS))
    np.add.at(H, (w_idx, w_idx),  w)
    np.add.at(H, (l_idx, l_idx),  w)
    np.add.at(H, (w_idx, l_idx), -w)
    np.add.at(H, (l_idx, w_idx), -w)
    H += np.eye(N_VARS) / (SIGMA_PRIOR**2)
    return H

x0 = np.zeros(N_VARS)
res = minimize(neg_log_posterior, x0, jac=grad_neg_log_posterior,
               method="L-BFGS-B",
               options={"maxiter": 2000, "ftol": 1e-10, "gtol": 1e-8})
print(f"MAP optimisation: {res.message}  | nlp={res.fun:.3f}")

theta_map = res.x

# --- Laplace approximation: Normal(θ*, H⁻¹) at MAP ---
H = hessian_neg_log_posterior(theta_map)
cov = np.linalg.inv(H)
eigs = np.linalg.eigvalsh(H)
assert eigs.min() > 0, f"Hessian not PD! min eig = {eigs.min()}"

# --- Posterior draws via multivariate normal sampling ---
N_DRAWS = 10_000
draws = rng.multivariate_normal(theta_map, cov, size=N_DRAWS)

# =============================================================================
# 6. Posterior summaries
# =============================================================================
theta_mean = draws.mean(axis=0)
theta_sd   = draws.std(axis=0)
theta_lo   = np.percentile(draws, 2.5, axis=0)
theta_hi   = np.percentile(draws, 97.5, axis=0)
prob_pos   = (draws > 0).mean(axis=0)

# Rank distribution: for each draw, rank variables (1 = best = highest θ)
ranks = (-draws).argsort(axis=1).argsort(axis=1) + 1  # 1-indexed
rank_mean = ranks.mean(axis=0)
rank_lo   = np.percentile(ranks, 2.5, axis=0)
rank_hi   = np.percentile(ranks, 97.5, axis=0)
prob_top3 = (ranks <= 3).mean(axis=0)
prob_top5 = (ranks <= 5).mean(axis=0)
prob_bottom5 = (ranks >= N_VARS - 4).mean(axis=0)

# All-vs-all dominance matrix
dom = np.zeros((N_VARS, N_VARS))
for i in range(N_VARS):
    dom[i] = (draws[:, i:i+1] > draws).mean(axis=0)
# dom[i,j] = P(θ_i > θ_j)

# =============================================================================
# 7. Assemble results
# =============================================================================
summary = []
for v in ALL_VARS:
    i = VAR_INDEX[v]
    n_papers = sum(1 for p in ALL_PAPERS.values() if v in p)
    summary.append({
        "var_id": v,
        "n_papers": n_papers,
        "theta_mean": float(theta_mean[i]),
        "theta_sd": float(theta_sd[i]),
        "theta_ci95_lo": float(theta_lo[i]),
        "theta_ci95_hi": float(theta_hi[i]),
        "prob_positive": float(prob_pos[i]),
        "rank_mean": float(rank_mean[i]),
        "rank_ci95_lo": float(rank_lo[i]),
        "rank_ci95_hi": float(rank_hi[i]),
        "prob_top3": float(prob_top3[i]),
        "prob_top5": float(prob_top5[i]),
        "prob_bottom5": float(prob_bottom5[i]),
    })

summary.sort(key=lambda r: -r["theta_mean"])

# =============================================================================
# 8. Write outputs
# =============================================================================
OUT_JSON = Path("/sessions/sharp-sweet-euler/pl_nma_results.json")
OUT_JSON.write_text(json.dumps({
    "config": {
        "n_papers": len(ALL_PAPERS),
        "n_vars": N_VARS,
        "n_pairs": len(pairs),
        "ref_var": "none (symmetric N(0,1) prior on each theta)",
        "sigma_prior": SIGMA_PRIOR,
        "n_draws": N_DRAWS,
        "method": "Bradley-Terry (Plackett-Luce pairwise reduction) + Laplace approximation",
    },
    "papers": {p: sorted(d.keys()) for p, d in ALL_PAPERS.items()},
    "variables": ALL_VARS,
    "summary": summary,
    "dominance_matrix": {
        ALL_VARS[i]: {ALL_VARS[j]: float(dom[i, j])
                      for j in range(N_VARS)}
        for i in range(N_VARS)
    },
    "map_nlp": float(res.fun),
    "hessian_min_eig": float(eigs.min()),
    "hessian_max_eig": float(eigs.max()),
}, indent=2))
print(f"Wrote {OUT_JSON}")

# =============================================================================
# 9. Sensitivity analyses
# =============================================================================
# We re-fit the model under two alternative evidence scopes and report where
# the headline ranking is robust vs. fragile.
#   S1: drop P2 and P3 (analytical-approximation runs) — keep only full-MCMC
#       BNMA (P1, P4) and the 8 systematic reviews.
#   S2: respect within-group structure — for each BNMA paper, split its
#       ranking into 4 sub-rankings (S, T, R, Overlay). This is the
#       scale-respecting fallback.
#
# All three fits share everything except the input pair set.

def fit(pair_list, label):
    global N_VARS  # use the master variable universe
    w = np.array([p[0] for p in pair_list])
    l = np.array([p[1] for p in pair_list])

    def nlp(theta):
        d = theta[w] - theta[l]
        return np.logaddexp(0.0, -d).sum() + 0.5 * (theta**2).sum() / SIGMA_PRIOR**2

    def gnlp(theta):
        d = theta[w] - theta[l]
        p = expit(-d)
        g = np.zeros(N_VARS)
        np.add.at(g, w, -p)
        np.add.at(g, l,  p)
        return g + theta / SIGMA_PRIOR**2

    def Hnlp(theta):
        d = theta[w] - theta[l]
        p = expit(d) * (1.0 - expit(d))
        H_ = np.zeros((N_VARS, N_VARS))
        np.add.at(H_, (w, w),  p)
        np.add.at(H_, (l, l),  p)
        np.add.at(H_, (w, l), -p)
        np.add.at(H_, (l, w), -p)
        H_ += np.eye(N_VARS) / SIGMA_PRIOR**2
        return H_

    x = np.zeros(N_VARS)
    r = minimize(nlp, x, jac=gnlp, method="L-BFGS-B",
                 options={"maxiter": 2000, "ftol": 1e-10, "gtol": 1e-8})
    H_ = Hnlp(r.x)
    C = np.linalg.inv(H_)
    d = rng.multivariate_normal(r.x, C, size=N_DRAWS)
    rk = (-d).argsort(axis=1).argsort(axis=1) + 1
    print(f"[{label}] nlp={r.fun:.2f}  n_pairs={len(pair_list)}")
    return {"theta_mean": d.mean(axis=0), "rank_mean": rk.mean(axis=0),
            "prob_top5": (rk <= 5).mean(axis=0), "n_pairs": len(pair_list)}

# --- S1: drop P2, P3 ---
pairs_S1 = [p for p in pairs if p[2] not in ("P2", "P3")]
S1 = fit(pairs_S1, "S1 (drop P2,P3)")

# --- S2: within-group BNMA rankings ---
# Build group membership from the within-paper S/T/R/Overlay structure as
# implied by the P1/P4 tables. Systematic reviews don't partition by group;
# they keep their full rankings as-is.
GROUP_OF = {
    # S
    "V003": "S", "V006": "S", "V007": "S", "V008": "S", "V011": "S",
    "V012": "S", "V013": "S", "V019": "S", "V028": "S",
    # T
    "V009": "T", "V010": "T", "V014": "T", "V017": "T", "V026": "T",
    # R
    "V001": "R", "V002": "R", "V004": "R", "V005": "R", "V015": "R",
    "V016": "R", "V018": "R", "V027": "R",
    # Overlay
    "C009_FaberTAA": "O", "C011_VIXTermStructure": "O",
    "C005_200DMA": "O", "C002_VIXTermSlope": "O", "C007_MarketBreadth": "O",
}

pairs_S2 = []
for paper_id in ("P1", "P2", "P3", "P4"):
    scores = ALL_PAPERS[paper_id]
    # sub-ranking per group
    by_group = {}
    for v, s in scores.items():
        g = GROUP_OF.get(v, "?")
        by_group.setdefault(g, []).append((v, s))
    for g, items in by_group.items():
        items.sort(key=lambda kv: -kv[1])
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i][1] > items[j][1]:
                    pairs_S2.append((VAR_INDEX[items[i][0]],
                                     VAR_INDEX[items[j][0]],
                                     f"{paper_id}.{g}"))
# systematic-review pairs unchanged
for p in pairs:
    if p[2] not in ("P1", "P2", "P3", "P4"):
        pairs_S2.append(p)
S2 = fit(pairs_S2, "S2 (within-group BNMA)")

# Attach to summary
for r in summary:
    i = VAR_INDEX[r["var_id"]]
    r["S1_theta_mean"] = float(S1["theta_mean"][i])
    r["S1_rank_mean"]  = float(S1["rank_mean"][i])
    r["S1_prob_top5"]  = float(S1["prob_top5"][i])
    r["S2_theta_mean"] = float(S2["theta_mean"][i])
    r["S2_rank_mean"]  = float(S2["rank_mean"][i])
    r["S2_prob_top5"]  = float(S2["prob_top5"][i])

# Re-write JSON with sensitivity columns
OUT_JSON.write_text(json.dumps({
    "config": {
        "n_papers": len(ALL_PAPERS),
        "n_vars": N_VARS,
        "n_pairs_primary": len(pairs),
        "n_pairs_S1": S1["n_pairs"],
        "n_pairs_S2": S2["n_pairs"],
        "sigma_prior": SIGMA_PRIOR,
        "n_draws": N_DRAWS,
        "method": "Bradley-Terry (Plackett-Luce pairwise reduction) + Laplace approximation",
        "ordinal_input_bnma": "p_beats_peers (joint-posterior peer-dominance)",
        "ordinal_input_reviews": "grade_numeric + 0.5*(class=EFFECTIVE) - 0.5*(class=INEFFECTIVE) + 0.3*sharpe",
    },
    "papers": {p: sorted(d.keys()) for p, d in ALL_PAPERS.items()},
    "variables": ALL_VARS,
    "summary": summary,
    "dominance_matrix": {
        ALL_VARS[i]: {ALL_VARS[j]: float(dom[i, j])
                      for j in range(N_VARS)}
        for i in range(N_VARS)
    },
    "map_nlp_primary": float(res.fun),
    "hessian_min_eig": float(eigs.min()),
    "hessian_max_eig": float(eigs.max()),
}, indent=2))
print(f"Wrote {OUT_JSON}")

print(f"\n=== Primary + sensitivity ranking ===")
print(f"{'rank':>4s}  {'var_id':<24s}  {'n':>3s}  {'theta':>7s}  {'95% CrI':>18s}  "
      f"{'S1_theta':>8s}  {'S2_theta':>8s}  {'P(top5)':>7s}")
for k, r in enumerate(summary, 1):
    ci = f"[{r['theta_ci95_lo']:>+5.2f}, {r['theta_ci95_hi']:>+5.2f}]"
    print(f"{k:>4d}  {r['var_id']:<24s}  {r['n_papers']:>3d}  "
          f"{r['theta_mean']:>+7.3f}  {ci:>18s}  "
          f"{r['S1_theta_mean']:>+8.3f}  {r['S2_theta_mean']:>+8.3f}  "
          f"{r['prob_top5']:>7.2f}")
