"""
Solve the differential equations for pendulum using scipy

https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html
"""

from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np

def pend(y, t, b, c):
    """
    Input: tuple y, floats t, b, c from model function for pendulum
    
    Output: Estimates of derivatives of y
    """
    theta, omega = y
    dydt = [omega, -b*omega - c*np.sin(theta)]
    return dydt


def plot_pendulum(t, sol):
    """
    Input: 1D numpy array t, 2D numpy array sol
    
    Action: Plot each coordinate of the solution vs t
    """

    plt.plot(t, sol[:, 0], 'b', label='theta(t)')
    plt.plot(t, sol[:, 1], 'g', label='omega(t)')
    plt.title("x and y coordinates of pendulum as a function of t")
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()


def solve_pendulum():
    """ Solve an example """
    
    y0 = [np.pi - 0.1, 0.0]
    t = np.linspace(0, 10, 101)
    sol = odeint(pend, y0, t, args=(0.25, 5.0))
    plot_pendulum(t, sol)
    
solve_pendulum()




