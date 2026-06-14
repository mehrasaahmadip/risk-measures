# Risk Measures: EVaR, CVaR, VaR

A clean Python implementation of risk measures — VaR, CVaR, and EVaR — with empirical estimation and comparison across distribution families.

This is the foundation for a larger project on risk-sensitive Best Arm Identification (BAI), where the goal will be to identify the arm with the lowest EVaR rather than the highest mean.

## Motivation

EVaR (Entropic Value at Risk) is an information-theoretic risk measure derived from the moment generating function. It is tighter than CVaR (Conditional Value at Risk) and more sensitive to tail behavior, making it a natural fit for risk-averse decision making under uncertainty.

## Project structure

```
evarbai/
├── Risk_measures_new.py    # EVaR, CVaR, VaR — RiskMeasures class
├── experiment_11J26.py     # distribution comparison experiment
├── notes.md                # Python engineering notes (quick reference)
└── notes.tex               # same notes as compilable LaTeX report
```

## Risk measures

Given samples from a distribution and a confidence level α ∈ (0,1):

- **VaR(α)** — the α-quantile; ignores what happens beyond the threshold
- **CVaR(α)** — expected value of losses exceeding VaR(α); accounts for tail shape
- **EVaR(α)** — tightest upper bound from the Chernoff family; strictly more conservative than CVaR

EVaR is computed via:

```
EVaR_α(X) = inf_{z>0} (1/z) [log E[e^{zX}] − log(1−α)]
```

The log-sum-exp trick is used for numerical stability in the MGF estimate.

## Observations: EVaR vs CVaR across distributions

The plot below compares EVaR and CVaR as α varies from 0.1 to 0.9 across four distributions.

| Distribution | Tail type | EVaR vs CVaR |
|---|---|---|
| Gaussian | Light, symmetric | Nearly identical across all α |
| Log-normal | Light, right-skewed | Mild divergence at high α |
| Pareto (shape=2) | Heavy, power-law | Large divergence at high α |
| Student-t (df=3) | Heavy, symmetric | Large divergence at high α |

**Key observation:** EVaR and CVaR agree on light-tailed distributions and diverge increasingly on heavy-tailed ones, with the gap growing as α → 1. This confirms that EVaR is a strictly tighter risk measure than CVaR, and the difference is practically significant only when tail risk is non-negligible.

## Planned algorithms

- [ ] LUCB (Lower Upper Confidence Bound) adapted for EVaR
- [ ] KL-LUCB with EVaR-based confidence bounds
- [ ] Track-and-Stop with EVaR as the target quantity

## Requirements

```
numpy
scipy
matplotlib
```
