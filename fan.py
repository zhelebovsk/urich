from matplotlib import pyplot as plt
import numpy as np

if __name__ == '__main__':
    ro = 1.2
    dk = 0.15
    dh = 0.07
    dm = (dk + dh) / 2.0

    nFan = 5000.0
    omegaFan = nFan / 60.0 * 2.0 * np.pi
    areaFan = np.pi / 4.0 * (dk*dk - dh*dh)

    uh = dh * omegaFan / 2.0
    um = dm * omegaFan / 2.0
    uk = dk * omegaFan / 2.0

    powerEng = 30
    flowRateT = np.power(2*powerEng*ro*ro*areaFan*areaFan, 1/3)
    vChT = flowRateT/ro/0.01
    caFan = flowRateT/areaFan/ro

    crk = caFan/uk
    crm = caFan/um
    crh = caFan/uh

    rostm = 1
    c2um = (1 - rostm) * 2 * um
    c2uh = (1 - rostm) * 2 * uh
    c2uk = (1 - rostm) * 2 * uk
    #w1m = um/(np.cos(np.arctan(caFan/um)))
    #deltawum = um - c2um
    #deltawuh = deltawum * dm /dh
    #deltawuk = deltawum * dm / dk