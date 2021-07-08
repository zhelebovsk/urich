import numpy as np


def f(g, cd, u, v, rof, rop, dp):
    return g + cd * rof / rop * 3.0 / 4.0 * np.abs(u-v) * (u-v) / dp


def f_plus(h, g, cd, u, v, rof, rop, dp):
    k1 = f(g, cd, u, v, rof, rop, dp)
    k2 = f(g, cd, u, v + k1 * h/2.0, rof, rop, dp)
    k3 = f(g, cd, u, v + k2 * h/2.0, rof, rop, dp)
    k4 = f(g, cd, u, v + k3 * h, rof, rop, dp)
    return v + h / 6 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)