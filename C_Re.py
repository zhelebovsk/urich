import numpy as np


def taup0(rop, dp, muf):
    return rop * dp * dp / 18.0 / muf
# TRUE


def Rep(u, v, dp, muf, rof):
    return np.abs(u - v) * dp / muf * rof


def cre(Rep):
    if Rep > 1000:
        return 0.11 * Rep / 6.0
    else:
        return 1 + np.power(Rep, 2.0 / 3.0) / 6.0


def Cd(Rep):
    return 24.0 / Rep * cre(Rep)


def Cdstk(Rep):
    return 24.0 / Rep


def taup(taup0, Rep):
    return taup0 / cre(Rep)


def wsettling(taup, a):
    return taup * a

def Stk(taup, u, r):
    return taup * u / r