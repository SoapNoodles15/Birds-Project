# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 13:22:10 2023
@author: Ja
"""
from  numpy import *
import numpy as np
from  matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pandas as pd
from scipy import special
import math
from matplotlib.animation import FuncAnimation


def f(x, ylim, alpha, t):
    return 0.5*(special.erf((ylim - x)/(np.sqrt(4*alpha*t))) - special.erf((-ylim - x)/(np.sqrt(4*alpha*t))))

x = np.linspace(-3,3,100)
t = 0.035
ylim = 0.5
alpha = 1

fig, ax = plt.subplots(figsize = (8,8))
line, = ax.plot(x, f(x, ylim, alpha, 0.0))
ax.set_title("Temperature at time t", fontsize = 15)
ax.set_xlabel("x [m]", fontsize = 15)
ax.set_ylabel("u(x)", fontsize = 15)
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='black')
def init():
    line.set_ydata(np.zeros_like(x))
    return line,

def update(t):
    line.set_ydata(f(x, ylim, alpha, t))
    time_text.set_text('Time = {:.3} seconds'.format(t))
    return line, time_text

ani = FuncAnimation(fig, update, frames=np.linspace(0, 5, 100), init_func=init, interval=150)
ani.save('C:/Users/Ja/Desktop/HT2023/Math Methods/Heat Lab/Task1Anim.mp4', writer='ffmpeg', fps=30)  # You may need to install the 'pillow' package if you haven't already

plt.show()


