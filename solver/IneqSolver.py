import numpy as np

class IneqSolver(object):
    def __init__(self, param_dict, linspace=np.linspace(0, 1, 1001)):
        self.param_dict = param_dict
        self.linspace = linspace
        self.solution = None
        self.inequlity = lambda f, t, bound1, bound2, params: (
            f(t, **params) <= bound2
        ) * (f(t, **params) >= bound1)

    def solve(self, func, bound1, bound2):
        self.solution = self.inequlity(func, self.linspace, bound1, bound2, self.param_dict)
        return self

    def get_interval(self):
        if np.linalg.norm(self.solution):
            start = np.argmax(self.solution)
            end = np.argmin(self.solution[start:])
            return [self.linspace[start], self.linspace[end]]
        else:
            return [0, 0]


def alpha(a_hat, I_p_hat, I_d_hat, I_t_hat):
    return np.exp(I_p_hat + I_d_hat + I_t_hat) * (1 + a_hat)


def I_p(t, I_p_hat):
    a = (1-1e-4**2)/(1-I_p_hat - 1e-4)**2 - 1
    return min(t/np.sqrt(1+a*t**2)+I_p_hat, 1)


def I_d(t, I_d_hat):
    c = np.log(2 * np.exp(1 - I_d_hat) - 1)
    return min(np.log(1 + np.exp(c * t)) - np.log(2) + I_d_hat, 1)


def I_t(t, I_t_hat):
    return max(I_t_hat * (1 - t ** 2), 0)


def I(t, I_p_hat, I_d_hat, I_t_hat):
    return I_p(t, I_p_hat) * I_d(t, I_d_hat) * I_t(t, I_t_hat)


def in_an_interval(array, interval):
    return [interval[0] < element < interval[1] for element in array]


entropy = np.vectorize(
    lambda t, a_hat, I_p_hat, I_d_hat, I_t_hat: 1
    - np.log(
        1 + alpha(a_hat, I_p_hat, I_d_hat, I_t_hat) * I(t, I_p_hat, I_d_hat, I_t_hat)
    )
)
