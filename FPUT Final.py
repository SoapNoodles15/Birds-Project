import numpy as np
import matplotlib.pyplot as plt

N = 32

I = np.identity(32)

def tridiagonal_matrix(n, main_diag_val, upper_diag_val, lower_diag_val):

    matrix = np.zeros((n, n))

    np.fill_diagonal(matrix, main_diag_val)

    np.fill_diagonal(matrix[1:], upper_diag_val)

    np.fill_diagonal(matrix[:, 1:], lower_diag_val)

    return matrix

A = tridiagonal_matrix(N-1, 2, -1, -1)

eigenvalues, eigenvectors = np.linalg.eig(A)

sorted_indices = np.argsort(eigenvalues)
sorted_eigenvalues = eigenvalues[sorted_indices]
sorted_eigenvectors = eigenvectors[:, sorted_indices]

w_n = sorted_eigenvectors / np.linalg.norm(sorted_eigenvectors, axis=0)
omega_n = np.sqrt(sorted_eigenvalues)

#%%Checking which eigenvectors looks like what, used for debugging
# x_axis = np.linspace(0, 1, len(w_n))

# for i in range(len(w_n)):
#     plt.plot(x_axis, w_n[:,i], marker='o', label = f'index: {i}')
#     plt.xlabel('Arbitrary X-axis')
#     plt.ylabel('Eigenvector (Smallest Eigenvalue)')
#     plt.title('Plot of Eigenvector Corresponding to Smallest Eigenvalue')
#     plt.grid(True)
#     plt.legend(loc = 2)
#     plt.show()
#     # print(np.dot(w_n[:,i],w_n[:,i]))

#%%Parameters and initial conditions
u = np.zeros(N+1)
u[1:N] = 4*w_n[:,0]

v = np.zeros(N+1)

nt = 50000
K = 1
M = 1
a = 3#0.25
dt = np.sqrt(1/8)
#%%Functions

def f(u,a):
    f = np.empty(len(u))
    for i in range(len(u)):
        
        ul = u[i - 1] if i - 1 >= 1 else 0
        u0 = u[i]
        ur = u[i + 1] if i + 1 < len(u)-1 else 0
        
        f[i] = ur + ul - 2 * u0 + a * ((ur - u0)**2 - (u0 - ul)**2)

    return f

def en(u, v, e_val, e_vec):
    xi = np.dot(e_vec, u[1:-1])
    dxi = np.dot(e_vec, v[1:-1])
    energy = 0.5*(dxi**2 + e_val**2 * xi**2)
    return energy

#%% Main loop
x_axis = np.linspace(0, 1, len(w_n)+2)#arbitrary x_axis for debugging plots

E1 = []
E2 = []
E3 = []
E4 = []
T = []

for j in range(nt):
    F1 = f(u,a)
    
    u = u + v*dt + 0.5*F1*dt**2
    u[0] = 0
    u[-1] = 0

    F2 = f(u,a)
    
    v = v + 0.5*(F1+F2)*dt
    v[0] = 0
    v[-1] = 0
    
    # plt.plot(x_axis,u) #plotting u at each step, used for debugging
    # plt.ylim(-1,1)
    # plt.show()
    
    e1 = 100*en(u,v,omega_n[0],w_n[:,0])
    e2 = 100*en(u,v,omega_n[1],w_n[:,1])
    e3 = 100*en(u,v,omega_n[2],w_n[:,2])
    e4 = 100*en(u,v,omega_n[3],w_n[:,3])
    if e1 > 1e2 or e2 > 1e2 or e3 > 1e2 or e4 > 1e2: #checking when energy is too high, used for debugging
        print(f'overflow at j = {j}')
        break
    E1.append(e1)
    E2.append(e2)
    E3.append(e3)
    E4.append(e4)
    
    arb_time = dt*j*omega_n[0]/(2*np.pi)
    T.append(arb_time)

#%% Plotting
xticks = np.linspace(0,160,9)

plt.figure(figsize=(8,7))

plt.plot(T,E1, label = 'k = 1')
plt.plot(T,E2, label = 'k = 2')
plt.plot(T,E3, label = 'k = 3')
plt.plot(T,E4, label = 'k = 4')

plt.xlim(0,160)
plt.ylim(0,8)

plt.xlabel(r"$\omega_1 t/2\pi$",fontsize=15)
plt.ylabel(r"$E_k(\times10^{-2})$",fontsize=15)
plt.title(r"$E_k$ vs cycles for k = 1, 2, 3, 4, $\alpha$ = 3", fontsize = 15)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)

plt.grid()
plt.legend(loc=1)
plt.show()