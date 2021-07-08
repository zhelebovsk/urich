import numpy as np
from matplotlib import pyplot as plt
import C_Re
import airprops
import RK


class Particles:
    def __init__(self, dp=160.0, rop=2550.0):
        self.dp = dp
        self.rop = rop


class Gas:
    def __init__(self, R=287.0, P=101325.0, T=288.15):
        self.R = R
        self.P = P
        self.T = T
        self.muf = airprops.mu_air(self.T)
        self.rof = airprops.density_air(self.R, self.P, self.T)


class Flow:
    def __init__(self, l=1.5, u=2.0, gas=Gas(), particle=Particles()):
        self.u = u
        self.gas = gas
        self.particles = particle
        self.l = l
        self.w_set_c = C_Re.w_settling_corrected(self.particles.rop,
                                                 self.particles.dp,
                                                 self.gas.muf,
                                                 self.gas.rof,
                                                 self.u,
                                                 9.81)

    def caaasmp(self):
        k = 50001
        i = 1
        dt = 0.00005
        self.v = np.zeros(k)
        self.Re_p = np.zeros(k - 1)
        self.cd = np.zeros(k - 1)
        self.time = np.zeros(k)
        self.x = np.zeros(k)
        while i < k:
            self.Re_p[i - 1] = C_Re.reynolds_particle(self.u,
                                                      self.v[i - 1],
                                                      self.particles.dp,
                                                      self.gas.muf,
                                                      self.gas.rof)
            self.cd[i - 1] = C_Re.c_drag(self.Re_p[i - 1])
            self.v[i] = RK.f_plus(dt,
                                  9.81,
                                  self.cd[i - 1],
                                  self.u,
                                  self.v[i - 1],
                                  self.gas.rof,
                                  self.particles.rop,
                                  self.particles.dp)
            self.x[i] = self.x[i - 1] + (self.v[i] + self.v[i - 1]) / 2.0 * dt
            self.time[i] = self.time[i - 1] + dt
            i += 1


if __name__ == '__main__':
    u = np.linspace(1,10,10)
    air = Gas(287.0, 101325.0, 288.15)
    partlist = [Particles(130.0 * np.power(10.0, -6)),
                Particles(160.0 * np.power(10.0, -6)),
                Particles(190.0 * np.power(10.0, -6))]
    flows = {}
    for i in partlist:
        f = {}
        for j in u:
            f[j] = Flow(1.5, j, air, i)
        flows[i.dp] = f
    for i in flows:
        print('dp = ', flows[i][1].particles.dp*1000000)
        for j in flows[i]:
            print('u = ', flows[i][j].u)
            flows[i][j].caaasmp()
    np.argmin(np.abs(flows[0.00013][1.0].x)-1.5)