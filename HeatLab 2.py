from numpy import *
import numpy as np
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pandas as pd
from scipy import special
import math
from matplotlib.animation import FuncAnimation

def f(r, rlim, alpha, t, init_temp):
    return 0.5 * init_temp * (special.erf((rlim - r) / (np.sqrt(4 * alpha * t))) - special.erf((-rlim - r) / (np.sqrt(4 * alpha * t))))

x = np.linspace(0, 50, 100)
deltax = 0.5
y = np.linspace(0, 50, 100)
deltay = 0.5
X, Y = np.meshgrid(x, y)
ylim = 0.5
xlim = 0.5
alpha = 1
init_temp = 100
r0x = 17.5
r0y = 37.5
rlim = 5/2

Z = np.zeros_like(X)

fig, ax = plt.subplots()
pcm = ax.pcolormesh(X, Y, Z, cmap='jet', shading='auto', vmax=init_temp)
plt.colorbar(pcm, label = 'Temperature [K]')
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Temperature at time t')
def update(frame):
    t = frame*0.1
    for i in range(len(x)):
        for j in range(len(y)):
            r = np.sqrt((i * deltax - r0x)**2 + (j * deltay - r0y)**2)
            Z[j, i] = f(r, rlim, alpha, t, init_temp)
    pcm.set_array(Z.ravel())
    time_text.set_text('t = {:.2} seconds'.format(t))
    return pcm, time_text

frames = 100 # Number of frames
animation = FuncAnimation(fig, update, frames=frames, interval=10, blit=True)
# animation.save('C:/Users/Ja/Desktop/HT2023/Math Methods/Heat Lab/Task2aAnim.mp4', writer='ffmpeg', fps=30)

plt.show()