# Risk Measures: EVaR, CVaR, and VaR

One important topic in fields such as finance, insurance, health, and agriculture is risk-sensitive decision making.

This project implements three classical risk measures — VaR, CVaR, and EVaR — and compares them empirically across distributions with different tail behaviors.

## What are these risk measures?

Given samples from a distribution and a confidence level α ∈ (0, 1), when we observe X as reward:

- **VaR(α)** is the α-quantile — a threshold below which α of outcomes fall. Simple, but it completely ignores what happens beyond that threshold.
- **CVaR(α)** is the expected value of outcomes that exceed VaR(α). It looks at the tail, not just the edge of it.
- **EVaR(α)** goes further. It is derived from the moment generating function and provides the tightest possible upper bound on tail risk within the Chernoff family. EVaR is always at least as large as CVaR — often significantly so on heavy-tailed distributions.

EVaR is computed by solving:

```
EVaR_α(X) = inf_{z>0} (1/z) [log E[e^{zX}] − log(1−α)]
```

The implementation uses the log-sum-exp trick for numerical stability when estimating the moment generating function from samples.

## What does the comparison show?

Running EVaR and CVaR across four distributions tells a clear story:

| Distribution | Tail behavior | EVaR vs CVaR |
|---|---|---|
| Gaussian | Light, symmetric | Almost identical — tails are negligible |
| Log-normal | Skewed, light tail | Small gap at high α |
| Pareto (shape=2) | Heavy, power-law | Large gap — EVaR is much more conservative |
| Student-t (df=3) | Heavy, symmetric | Large gap — same story |

The gap between EVaR and CVaR grows with tail heaviness and with α. On a Gaussian, the two measures are nearly interchangeable. On a Pareto or Student-t, EVaR can be substantially larger — which matters when the cost of a bad outcome is high.


## Requirements

```
numpy
scipy
matplotlib
```
