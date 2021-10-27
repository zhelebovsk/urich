import numpy as np
import airprops


def tau_particle_0(rop, dp, muf):
    return rop * dp * dp / 18.0 / muf


def reynolds_particle(u, v, dp, muf, rof):
    return np.abs(u - v) * dp / muf * rof


def correction_reynolds(rep):
    if rep > 1000:
        return 0.11 * rep / 6.0
    else:
        return 1.0 + np.power(rep, 2.0 / 3.0) / 6.0


def c_drag(rep):
    return 24.0 / rep * correction_reynolds(rep)


def c_drag_stk(rep):
    return 24.0 / rep


def tau_particle(taup0, rep):
    return taup0 / correction_reynolds(rep)


def w_settling(taup, a=9.81):
    return taup * a


def stokes(taup, u, r):
    return taup * u / r


def w_settling_corrected(rop, dp, muf, rof, u, a=9.81):
    taup0 = tau_particle_0(rop, dp, muf)
    # Время динамической релаксации частицы с учетом поправки
    w = 1000.0
    w0 = 2.0 * w
    while np.abs(w-w0)/w > np.power(10.0, -6):  # повторять цикл пока разница между скоростью витания и факт выше 0.5%
        w0 = w
        Rep = reynolds_particle(u, u + w, dp, muf, rof)
        taup = tau_particle(taup0, Rep)
        # Скорость витания (гравитационного) и коэффициенты сопротивления
        cd = c_drag(Rep)
        w = w_settling(taup, a)
    return w#, cd, taup, Rep,


if __name__ == "__main__":
    rop = 2550.0
    dp = 160.0 * np.power(10.0, -6)
    #muf = 1.79 * np.power(10.0, -5)
    T = 288.15
    muf = airprops.mu_air(T)
    #print(muf)
    u = 2.5
    rof = 1.22
    #rof = airprops.density_air(r_gas=287.0, p=101325, t=T)

    #print(rof)
    w = w_settling_corrected(rop, dp, muf, rof, u)
    print(w)
    #taup, Rep, w, cd = w_settling_corrected(rop, dp, muf, u)
    #w0 = w_settling(tau_particle_0(rop, dp, muf))
    #print('taup = ', taup)
    #print('Rep = ', Rep)
    #print('w = ', w)
    #print('cd = ', cd)
    #print('w/w0 = ', w/w0)
