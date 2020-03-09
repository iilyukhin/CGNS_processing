import matplotlib.pyplot as plt

def plot_over_y(x):
    node_x = get_node_x(x)
    y, vx = get_xcolumn(node_x, 'VelocityX')
    plt.plot(vx,y, 'o', markersize = 0.5)
    plt.xlim(0, 1)
    plt.ylim(0, 0.005)
    plt.grid(True)
    plt.title('Профиль скорости в сечении x = ' + str(x))
    plt.ylabel('y')
    u_min = min(vx)
    plt.text(0.2, 0.0025, '$u_{min} = $' + str(u_min))
    plt.xlabel('$u/u_{\infty}$')
    plt.show()
