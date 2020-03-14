#Processing of txt files, which were taken from CGNS

"""
get_data:
input: file_name (str)
output: var_names (array of str),
        data (array of data arrays, float)
        x_points (array of x coordinates)
"""

def get_data(file_name):

    f = open(file_name)
    names = f.readline()
    data = f.readlines()
    f.close()


    var_names = names.split()
    num_vars = len(var_names)
    clear_data = []
    x_points = []
    N = len(data)
    i = 0
    for line in data:
        i+=1
        if (int(i/N*100) != int((i-1)/N*100)) and (int(i/N*100)%10 == 0):
            print(file_name + '...' + str(int(i/N*100)) + '%')
        splitted_line = line.split()
        if len(splitted_line) == num_vars:
            float_s_line = []
            for char in splitted_line:
                float_s_line.append(float(char))
            clear_data.append(float_s_line)
            if (var_names[0] == 'CoordinateX'):
                x = float_s_line[0]
                if not (x in x_points):
                    x_points.append(x)
    return var_names, clear_data, x_points

def sort_arrays(y, f_y):
    presort = []
    for i in range(len(y)):
        presort.append([y[i], f_y[i]])

    presort.sort(key = lambda x: x[0])
    y_sorted = []
    var_sorted = []
    for i in range (len(y)):
        y_sorted.append(presort[i][0])
        var_sorted.append(presort[i][1])
    return y_sorted, var_sorted

'''
get_xcolumn: collects variable over y in choosen x slice
input:  x (x slice)
        var_name
        var_names
        data

output: y_column (array of float)
        var_column (array of float)
'''

def get_xcolumn(x, var_name, var_names, data):

    num_column = var_names.index(var_name)

    var_column = []
    y_column = []

    for line in data:
        if line[0] == x:
            y_column.append(line[1])
            var_column.append(line[num_column])

    y, var = sort_arrays(y_column, var_column)
    return y, var

def get_node_x(approximate_x, x_points):
    node_x = 0
    if approximate_x in x_points:
        return approximate_x
    else:
        for x in x_points:
            if abs(x - approximate_x) < abs(node_x - approximate_x):
                node_x = x
        return node_x

def get_xline(var_name, var_names, data, y = 0):
    num_column = var_names.index(var_name)
    var_column = []
    x_array = []
    for line in data:
        if line[1] == y:
            x_array.append(line[0])
            var_column.append(line[num_column])
    return x_array, var_column
