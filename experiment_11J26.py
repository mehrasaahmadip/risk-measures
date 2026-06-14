import numpy as np
from numpy import random
import scipy.stats as stats
import matplotlib.pyplot as plt
from Risk_measures_new import RiskMeasures

alpha_range = np.arange(0.1, 0.9, 0.1)
n = 10000

distributions = {
    'Gaussian':  random.normal(0, 1, n),
    'Log-normal': random.lognormal(0, 1, n),
    'Pareto':    random.pareto(2, n),       # shape=2, heavy tail
    'Student-t': stats.t.rvs(df=3, size=n) # df=3, very fat tail
}
fig, ax = plt.subplots(2, 2, figsize=(10, 8))
axes = ax.flatten()

for i, (name, samples) in enumerate(distributions.items()):
    hist_e = []
    hist_c = []
    for alpha in alpha_range:
        exp = RiskMeasures(samples, alpha)
        hist_e.append(exp.EVaR())
        hist_c.append(exp.CVaR())

    axes[i].plot(alpha_range, hist_c, label='CVaR')
    axes[i].plot(alpha_range, hist_e, label='EVaR')
    axes[i].set_xlabel('Alpha')
    axes[i].set_ylabel('Risk Measure')
    axes[i].set_title(f'{name}')
    axes[i].legend()
    axes[i].grid(True)

plt.tight_layout()
plt.show()

