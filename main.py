import numpy as np
from matplotlib import pyplot as plt
import C_Re
import airprops
import RK


class Particles:
    def __init__(self, dp, rop):
        self.dp = dp
        self.name = int(dp*1000000)
        self.rop = rop

    def __repr__(self):
        return "[dp = " + str(self.name) + ", rop = " + str(self.rop) + "]"


class Gas:
    def __init__(self, R, P, T):
        self.R = R
        self.P = P
        self.T = T
        self.muf = airprops.mu_air(self.T)
        self.rof = airprops.density_air(self.R, self.P, self.T)

    def __repr__(self):
        return "[R = " + str(self.R) + ", P = " + str(self.P) + " , T = " + str(self.T) + "]"


class Flow:
    def __init__(self, l, u, gas, particle):
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

    def __repr__(self):
        return "u = " + str(self.u) + ", particles: " + repr(self.particles)

    def caaasmp(self):
        k = 80001
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
    """def caaasmp_height(self):
        k = 10001
        i = 1
        dt = 0.00005
        #self.vh = - self.v[-1] * np.ones(k)
        self.vh = - 1 * self.v[self.l_element] * np.ones(k)
        #self.vh = np.zeros(k)
        #self.v = -np.ones(k)*31
        self.Re_ph = np.zeros(k - 1)
        self.cdh = np.zeros(k - 1)
        self.timeh = np.zeros(k)
        self.xh = np.zeros(k)
        while self.vh[i-1] < 0:
            self.Re_ph[i - 1] = C_Re.reynolds_particle(self.u,
                                                      self.vh[i - 1],
                                                      self.particles.dp,
                                                      self.gas.muf,
                                                      self.gas.rof)
            self.cdh[i - 1] = C_Re.c_drag(self.Re_ph[i - 1])
            self.vh[i] = RK.f_plus(dt,
                                  9.81,
                                  self.cdh[i - 1],
                                  self.u,
                                  self.vh[i - 1],
                                  self.gas.rof,
                                  self.particles.rop,
                                  self.particles.dp)
            self.xh[i] = self.xh[i - 1] + (self.vh[i] + self.vh[i - 1]) / 2.0 * dt
            self.timeh[i] = self.timeh[i - 1] + dt
            self.height = self.xh[i]
            i += 1


    def velocity_lenght(self):
        self.l_element = np.argmin(np.abs(self.x - self.l))"""


if __name__ == '__main__':
    air = Gas(287.0, 101325.0, 293.15)

    u = np.linspace(-20,0.0001,5)
    partlist = [Particles(160*1e-6, 2550.0), Particles(8000*1e-6, 1000.0)]

    flows = []

    for velocity in u:
        for p in partlist:
            #flows[velocity, p] = Flow(3.0, velocity, air, p)
            flows.append(Flow(3.0, velocity, air, p))

    for flow in flows:
        flow.caaasmp()

    for flow in flows:
        if flow.particles.name == 160:
            plt.plot(flow.x, flow.v, linestyle="--")
        else:
            plt.plot(flow.x, flow.v)
    plt.grid()
    plt.show()
    #for flow in flows:
    #    print(flow, ":")
    #    flow.caaasmp()
    #    print("-------------------------")
    """for i in partlist:
        f = {}
        for j in u:
            f[j] = Flow(3.0, j, air, i)
        flows[i.dp] = f
    for i in flows:
        for j in flows[i]:
            print('u = ', flows[i][j].u)
            flows[i][j].caaasmp()
            flows[i][j].velocity_lenght()
            flows[i][j].caaasmp_height()
    for i in flows:
        v = []
        u = []
        h = []
        for j in flows[i]:
            indx = flows[i][j].l_element
            #v.append(flows[i][j].v[indx]-flows[i][j].u)
            v.append(flows[i][j].v[indx]-flows[i][j].u)
            u.append(flows[i][j].u)
            h.append(-flows[i][j].height)
        plt.plot(u,v)
    #plt.axhline(1.069)
    plt.grid(True)
    plt.show()
    plt.plot(u, h)
    plt.show()"""