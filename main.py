from matplotlib import pyplot as plt
import numpy as np
import C_Re

dp = 200.0 * np.power(10.0, -6)
muf = 1.78 * np.power(10.0, -5)
rof = 1.24
rop = 2550.0
r = 0.015 / 2.0# радиус паяльника
a = b = 0.1
h = 0.5

u = 10.0
v = 10.4

taup0 = C_Re.taup0(rop, dp, muf)
Rep = C_Re.Rep(u, v, dp, muf, rof)

taup = C_Re.taup(taup0, Rep)
print(taup0, taup, Rep)

cd = C_Re.Cd(Rep)
cd1 = C_Re.Cdstk(Rep)
print(cd, cd1)

w = C_Re.wsettling(taup, 9.81)
print(w)

Stk = C_Re.Stk(taup, u, r)
print(Stk)
