"""
Calculating new wages using the labor market clearing condition
"""

import numpy as np


def lmc(Xp, Dinp, J, N, B, VAL):
    PQ_vec = Xp.T.reshape(J * N, 1, order='F').copy()

    DDinpt = np.zeros((J * N, N))
    for n in range(N):
        DDinpt[:, n] = Dinp[:, n] * PQ_vec

    DDDinpt = np.zeros((N, J * N))
    for n in range(N):
        DDDinpt[n, :] = sum(DDinpt[n * N: (n + 1) * N, :])

    aux4 = B * DDDinpt
    aux5 = sum(aux4)
    aux5 = aux5.T
    wf0 = (1 / VAL) * aux5
    
    return wf0
