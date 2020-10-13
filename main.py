from matplotlib import pyplot as plt
import numpy as np
import C_Re

# Время динамической релаксации стоксовой частицы
rop = 2550.0
dp = 200.0 * np.power(10.0, -6)
muf = 1.78 * np.power(10.0, -5)
taup0 = C_Re.taup0(rop, dp, muf)
print('taup0 = ', taup0)
# Время динамической релаксации частицы с учетом поправки
u = 0
v = 10.4107
rof = 1.24
Rep = C_Re.Rep(u, v, dp, muf, rof)
print('Rep = ', Rep)
taup = C_Re.taup(taup0, Rep)
print('taup = ', taup)
# Скорость витания (гравитационного) и коэффициенты сопротивления
cd = C_Re.Cd(Rep)
cdstk = C_Re.Cdstk(Rep)
w = C_Re.wsettling(taup, 9.81)
print('w = ', w)
# Определение числа стокса (размер паяльника - характерный размер)
rbody = 0.017 / 2.0
Stk = C_Re.Stk(taup, u, rbody)
print('Stk = ', Stk)
# Массовая концентрация
a = b = 0.1
Gp = 0.001
concM = Gp / (v * (a * b - Gp / (v * rop)) * rof)
concF = concM * rof / rop
print('Fi = ', concF)
