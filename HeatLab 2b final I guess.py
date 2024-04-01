from numpy import *
import numpy as np
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pandas as pd
from scipy import special
import math
from matplotlib.animation import FuncAnimation

def f(r, rlim, alpha, t, init_temp, tau):
    return np.exp(-t/tau)*0.5 * init_temp * (special.erf((rlim - r) / (np.sqrt(4 * alpha * t))) - special.erf((-rlim - r) / (np.sqrt(4 * alpha * t))))

x = np.linspace(0, 7e6, 100)
deltax = 0.7*1e5
y = np.linspace(0, 7e6, 100)
deltay = 0.7*1e5
X, Y = np.meshgrid(x, y)
ylim = 5
xlim = 5
alpha = 1
init_temp = 1e6
r0x = 45e5
r0y = 45e5
rlim = 1e4
tau = 100e16

Z = np.zeros_like(X)

fig, ax = plt.subplots()
pcm = ax.pcolormesh(X, Y, Z, cmap='jet', shading='auto', vmax=10000)
plt.colorbar(pcm, label = 'Temperature [K]')

alpha_core = 1e-5
alpha_outcore = 5*1e-5
alpha_incrust = 1e-6
alpha_crust = 5*1e-6


ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('Heat diffusion in Earth')
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white')
def update(frame):
    
    t = frame*1e16
    t_years = t / (365.25 * 24 * 3600 * 1e9)
    for i in range(len(x)):
        for j in range(len(y)):
            r = np.sqrt((i * deltax - r0x)**2 + (j * deltay - r0y)**2)
            if (i * deltax - 0)**2 + (j * deltay - 0)**2 <= (1.1e6)**2:
                Z[j, i] = 6000 + f(r, rlim, alpha_core, t, init_temp, tau)
            elif (i * deltax - 0)**2 + (j * deltay - 0)**2 <= (3.5e6)**2 and (i * deltax - 0)**2 + (j * deltay - 0)**2 > (1.1e6)**2:
                Z[j, i] = 4000 + f(r, rlim, alpha_outcore, t, init_temp, tau)
            elif (i * deltax - 0)**2 + (j * deltay - 0)**2 <= (6.2e6)**2 and (i * deltax - 0)**2 + (j * deltay - 0)**2 > (3.5e6)**2:
                Z[j, i] = 3000 + f(r, rlim, alpha_incrust, t, init_temp,tau)
            elif (i * deltax - 0)**2 + (j * deltay - 0)**2 <= (6.371e6)**2 and (i * deltax - 0)**2 + (j * deltay - 0)**2 > (6.2e6)**2:
                Z[j, i] = 300 + f(r, rlim, alpha_crust, t, init_temp,tau)    
            else:# (i * deltax - 0)**2 + (j * deltay - 0)**2 > 40**2:
                Z[j, i] = f(r, rlim, 0, t, init_temp,tau)
            # else:
            #     Z[j, i] = f(r, rlim, alpha, t, init_temp)
    pcm.set_array(Z.ravel())
    time_text.set_text('Time = {:.3} Gyrs'.format(t_years))
    
    return pcm, time_text

frames = 1000 # Number of frames
animation = FuncAnimation(fig, update, frames=frames, interval=10, blit=True)
# animation.save('C:/Users/Ja/Desktop/HT2023/Math Methods/Heat Lab/Task2bAnim.mp4', writer='ffmpeg', fps=15)

plt.show()