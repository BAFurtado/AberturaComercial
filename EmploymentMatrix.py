import pandas as pd
import numpy as np

sectors = pd.read_csv('C:/Users/r1702898/Documents/DISET/AberturaComercial/ModeloPythonAbertura/sectors.csv', sep=";", header=0)
matrix = np.zeros([58, 58])
for i in range(58):
    temp = np.ones(58)
    temp[i] = 513
    temp2 = np.random.dirichlet(temp, size=1)
    for j in range(58):
        matrix[i][j] = temp2[0][j]

print(matrix)
print(matrix.sum(axis=1))
print(matrix[0][0])
np.savetxt("matrix.txt", matrix, delimiter=" ", fmt='%1.14f')
