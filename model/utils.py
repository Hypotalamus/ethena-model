from typing import List
import numpy as np

def is_shock(curr_time: float, prev_time: float, shock_times: List[float]) -> bool:
    res = False
    if curr_time == prev_time == 0.0:
        res = True
    else:
        for shock_time in shock_times:
            if curr_time < shock_time:
                break
            elif prev_time < shock_time <= curr_time:
                res = True
                break

    return res

def runge_kutta4(y, x, dx, f):
    """computes 4th order Runge-Kutta for dy/dx.
    y is the initial value for dependent variable
    x is the initial value for argument
    dx is the difference in x (e.g. the time step)
    f is a callable function (y, x) that you supply 
    to compute dy/dx for the specified values.
    """    
    k1 = dx * f(y, x)
    k2 = dx * f(y + 0.5 * k1, x + 0.5 * dx)
    k3 = dx * f(y + 0.5 * k2, x + 0.5 * dx)
    k4 = dx * f(y + k3, x + dx)
    
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.

def runge_kutta4_system(y, x, dx, funcs):
    """computes 4th order Runge-Kutta for system of two ODEs (for dy/dx).
    y is the initial value for state
    x is the initial value for argument
    dx is the difference in x (e.g. the time step)
    f is a callable function (y, x) that you supply 
    to compute dy/dx for the specified values.
    """
    f, g = funcs    
    k1 = dx * f(y, x)
    l1 = dx * g(y, x)
    s1 = np.array([k1, l1])
    k2 = dx * f(y + 0.5 * s1, x + 0.5 * dx)
    l2 = dx * g(y + 0.5 * s1, x + 0.5 * dx)
    s2 = np.array([k2, l2])
    k3 = dx * f(y + 0.5 * s2, x + 0.5 * dx)
    l3 = dx * g(y + 0.5 * s2, x + 0.5 * dx)
    s3 = np.array([k3, l3])
    k4 = dx * f(y + s3, x + dx)
    l4 = dx * g(y + s3, x + dx)
    s4 = np.array([k4, l4])
    
    return list(y + (s1 + 2 * s2 + 2 * s3 + s4) / 6.)