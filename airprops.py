import numpy as np


def mu_air(t=288.15):
    return 1.458 * np.power(0.1, 6) * np.power(t, 1.5) / (t + 110.4)


def mu_air_sut(t=288.15):
    return 1.78 * np.power(0.1, 5) * np.power(t/273.0, 1.5) * (273.0 + 122.0)/(t + 122.0)



def density_air(r_gas=287.0, p=101325.0, t=288.15):
    return p / r_gas / t


if __name__ == '__main__':
    for i in range(273,2000,10):
        print(i-273, '   ',100*(mu_air(i+0.15)  - mu_air_sut(i + 0.15))/mu_air(i+0.15))

