#Processing of txt files, which were taken from CGNS

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

def get_xcolumn(x, var_name, var_names, data):
    num_column = var_names.index(var_name)
    var_column = []
    y_column = []
    for line in data:
        if line[0] == x:
            y_column.append(line[1])
            var_column.append(line[num_column])
    return y_column, var_column

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
