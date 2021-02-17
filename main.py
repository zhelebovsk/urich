from matplotlib import pyplot as plt
import numpy as np
import C_Re


def calc(rop, dp, muf, a, b, Gp, u, rbody):
    taup0 = C_Re.taup0(rop, dp, muf)
    # Время динамической релаксации частицы с учетом поправки
    w = 10000.0
    w0 = 2.0 * w
    while np.abs(w-w0)/w > np.power(10.0, -6):  # повторять цикл пока разница между скоростью витания и факт выше 0.5%
        w0 = w
        Rep = C_Re.Rep(u, u + w, dp, muf, rof)
        taup = C_Re.taup(taup0, Rep)
        # Скорость витания (гравитационного) и коэффициенты сопротивления
        cd = C_Re.Cd(Rep)
        cdstk = C_Re.Cdstk(Rep)
        w = C_Re.wsettling(taup, 9.81)
    v = u + w
    #print('v = ', v)
    # Определение числа стокса (размер паяльника - характерный размер)
    Stk = C_Re.Stk(taup, u, rbody)
    Stk0 = C_Re.Stk(taup0, u, rbody)
    # Массовая концентрация
    concM = Gp / (v * (a * b - Gp / (v * rop)) * rof)
    concF = concM * rof / rop
    return taup, Rep, v, w, cd, Stk, concM, concF


# Время динамической релаксации стоксовой частицы
rop = 2550.0
dp = 200.0 * np.power(10.0, -6)
muf = 1.78 * np.power(10.0, -5)
a = b = 0.1
Gp = 0.001
u = 2.0
rof = 1.24
rbody = 0.017 / 2.0
#taup, Rep, v, w, cd, Stk, concM, concF = calc(rop, dp, muf, a, b, Gp, u, rbody)


#u = np.linspace(1, 10, 11)
Gp = np.linspace(0.001, 0.1, 100)

sz = np.size(Gp)
v = np.zeros(sz)
taup = np.zeros(sz)
Rep = np.zeros(sz)
w = np.zeros(sz)
cd = np.zeros(sz)
Stk = np.zeros(sz)
concM = np.zeros(sz)
concF = np.zeros(sz)

i = 0
for var in Gp:
    taup[i], Rep[i], v[i], w[i], cd[i], Stk[i], concM[i], concF[i] = calc(rop, dp, muf, a, b, var, u, rbody)
    i = i + 1
plt.plot(Gp, concM)
plt.show()