"""
Solve the differential equation y'(t) = y(t) using scipy
"""

from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np

def exp(y, t):
    """
    Input: tuple y, floats t from model function for exponential
    
    Output: Estimates of derivative of y
    """
    yt, = y
    dydt = [yt]
    return dydt


def plot_exp(t, sol):
    """
    Input: 1D numpy array t, 1D numpy array sol
    
    Action: Plot each coordinate of the solution vs t
    """

    plt.plot(t, sol, 'b', label='y(t)')
    plt.title("Solution of y'(t) = y(t) with y(0) = 1")
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()


def solve_exp():
    """ Solve an example """
    
    y0 = (1)
    t = np.linspace(0, 1, 101)
    sol = odeint(exp, y0, t)
    print(sol)
    plot_exp(t, sol)
    
solve_exp()