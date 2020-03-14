#File with functions of the flow

import numpy as np
from physical_conditions import *

T_mu = 110.4/T_inf

def Re_x (x):
    return Re*x

def mu (T):
    return (1+T_mu)/(T+T_mu)*T**(3/2)

# безразмерное напряжение трения перед областью взаимодействия в невозмущённом ПС
a = 333
# вязкость на стенке перед областью взаимодействия
mu_w = mu(T_w)

#function to shift the array
def shift_x(x_array, x_0):
    x_shifted = []
    for x in x_array:
        x_shifted.append(x - x_0)
    return x_shifted

#Принимаем массив и координату х,
#отдаём массив в автомодельных координатах

def phys2ss(array, x):
    ss_array = []
    for item in array:
        ss_array.append(item*(Re_x(1)/x)**(1/2))
    return ss_array

#аппроксимация значения в заданной точке по двум ближайшим
def approx(V, x, x_p):
    i = 0
    for item in x:
        if abs(item - x_p) < abs(x[i] - x_p):
            i = x.index(item)
    if i == 0:
        print(V[0])
        return V[0]
    k1 = (x_p-x[i])*(x_p-x[i+1])/((x[i-1]-x[i])*(x[i-1]-x[i+1]))
    k2 = (x_p-x[i-1])*(x_p-x[i+1])/((x[i]-x[i-1])*(x[i]-x[i+1]))
    k3 = (x_p-x[i])*(x_p-x[i-1])/((x[i+1]-x[i])*(x[i+1]-x[i-1]))
    result = k1*V[i-1]+k2*V[i]+k3*V[i+1]
    return result


#работает только при условии, что dUdY имеет ровно два нуля на x
def get_x_separation(x, dU_dY):
    N = len(x)
    x_separation = 1.0
    rec_zone_len = 1.0
    for i in range (N-1):
        if x[i] >= 0.2:
            if dU_dY[i]*dU_dY[i+1] <= 0:
                x0 = dU_dY[i]/(dU_dY[i]-dU_dY[i+1])*(x[i+1]-x[i])
                if x_separation > x0:
                    x_separation = x0 + x[i]
                    break
    return x_separation


def get_rec_zone_len(x, x_separation, dU_dY):
    N = len(x)
    for i in range(N):
        if x[i] > x_separation:
            if dU_dY[i]*dU_dY[i+1] <= 0:
                rec_zone_len = x[i] + dU_dY[i]/(dU_dY[i]-dU_dY[i+1])*(x[i+1]-x[i]) - x_separation
                break
    return rec_zone_len


def calc_grad(x, f):
    N = len(x)
    grad = np.zeros(N)
    h = x[1]-x[0]
    for i in range(N):
        if i == 0:
            grad[0] = (f[1] - f[0])/h
        elif i == N-1:
            grad[N-1] = (f[N-1]-f[N-2])/h
        else:
            grad[i] = (f[i+1] - f[i-1])/(2*h)
    return grad

def calc_displ_thickness(y_array, u_array, u_e):

    N = len(y_array)
    disp_thick = 0
    step = y_array[1] - y_array[0]

    for u in u_array:
        i = u_array.index(u)
        if (0.97*u_e > u) and (y_array[i+1] - y_array[i] == step):
            disp_thick += step*u
        else:
            break

    if u[N-1] < 0.97*u_e:
        print('WARNING! u_max < 0.97*u_e')

    return disp_thick
