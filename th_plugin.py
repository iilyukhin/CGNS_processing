import numpy as np

T_inf = 293.0

T_w = T_inf*2.517

T_mu = 110.4/T_inf

Re = 2*10**6



def Re_x (x):
    return Re*x


def mu (T):
    return (1+T_mu)/(T+T_mu)*T**(3/2)

# безразмерное напряжение трения перед областью взаимодействия в невозмущённом ПС
a = 333
# вязкость на стенке перед областью взаимодействия
mu_w = mu(T_w)
# Число Маха
M = 3


def get_col(file_name, col_number = 0):

    col = []

    file = open(file_name)
    data = file.readlines()
    file.close()

    for line in data:
        try:
            value = float(line.split()[col_number])
            col.append(value)
        except:
            next

    return col

def get_ksi(x_physical, p):
    num_points = len(p)
    ksi = np.zeros(num_points)
    for i in range (num_points):
        ksi[i] = ((((2*(M**2-1)**(1/2))/(a*((Re_x(x_physical[i]))**(-0.5))*mu_w)))**(1/2))*p[i]
    return ksi


def get_x_locale(x, x_separation):
    N = len(x)
    x_locale = np.zeros(N)
    for i in range (N):
        x_locale[i] = x[i] - x_separation
    return x_locale


def count_lines(file_name):
    
    file = open(file_name)
    num_lines = sum(1 for line in file)
    file.close()
    
    return num_lines


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


def check_lines (file_name1, file_name2):
    
    file1 = open(file_name1)
    N1 = sum(1 for line in file1)
    file1.close()

    file2 = open(file_name2)
    N2 = sum(1 for line in file2)
    file2.close()

    if N1 != N2:
        print ("ОШИБКА!!!")


def calc_gradP(x,p):
    N = len(x)
    gradP = np.zeros(N)
    h = x[1]-x[0]
    for i in range(N):
        if i == 0:
            gradP[0] = (p[1] - p[0])/h
        elif i==N-1:
            gradP[N-1] = (p[N-1]-p[N-2])/h
        else:
            gradP[i] = (p[i+1] - p[i-1])/(2*h)
    return gradP
