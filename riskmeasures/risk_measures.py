import numpy as np
from scipy.optimize import minimize_scalar


class RiskMeasures:
    def __init__(self, samples, alpha):
        self.samples = samples
        self.alpha = alpha
        self.var = 0
        self.cvar = 0
        self.evar = 0

    def Compare(self):
        var = np.percentile(self.samples, 100 * self.alpha)
        cvar = self.CVaR()
        evar = self.EVaR()
        print(cvar)
        print(evar)
        print(var)

    def EVaR(self):
        def f(z, alp, s):
            c = z * np.max(s)
            log_mgf = c + np.log(np.mean(np.exp(z * s - c)))
            return (1/z) * (log_mgf - np.log(1 - alp))

        res = minimize_scalar(f, bounds=(1e-6, 100), method='bounded', args=(self.alpha, self.samples))
        self.evar = res.fun
        return res.fun

    def VaR(self):
        self.var = np.percentile(self.samples, 100 * self.alpha)
        return self.var

    def CVaR(self):
        self.VaR()
        C = self.samples[self.samples >= self.var]
        self.cvar = np.mean(C)
        return self.cvar
