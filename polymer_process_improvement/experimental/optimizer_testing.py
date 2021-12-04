import scipy.optimize as opt
import numpy as np


def calfun(k):
    """Example calibration function"""
    return k * 2 * 4


def IVcal(rho, alpha, k):
    """Example test function"""
    return rho * alpha * k


def error_function(x0, **args):
    """Calculates error between functions with current inputs"""
    xaxis = np.linspace(0.006, 0.036, 20)
    calibrate = np.array([calfun(K) for K in xaxis])
    smiledata = np.array([IVcal(x0[0], x0[1], K) for K in xaxis])

    # Get error between data
    error = smiledata - calibrate

    # Print square root of sum of errors
    print(np.sqrt(np.sum(error**2.0)))

    return error


# Initial guesses
rho = 2.5
alpha = 3.5
x0 = np.array([rho, alpha])

# Run optimisation
result = opt.leastsq(func=error_function, x0=x0)[0]
print('opt rho: ', result[0])
print('opt alpha: ', result[1])