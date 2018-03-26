import numpy as np


# Function to read data sets
def read_data(data_to_read):
    data_container = []
    for each in data_to_read:
        temp = np.loadtxt('./{}.txt'.format(each))
        data_container.append(temp)
    return data_container


# Necessary data, provided by Caliendo e Parro, 2014
tables = ['B', 'GO', 'IO', 'T', 'tariffs1993', 'tariffs2005', 'xbilat1993']
B, GO, IO, T, tariffs1993, tariffs2005, xbilat1993 = read_data(tables)

# Other needed parameters
vfactor = -.2
tol = 1E-07
maxit = 1E+10
J = 40
N = 31
