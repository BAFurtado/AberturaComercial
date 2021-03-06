""" This function calculates de Omega matrix in Caliendo - Parro (2009)
 Inputs are A = alphas, B = bethas, G = I-O matrix, Dinp = trade shares,
 tarifap = tarifs, Fp = trade weighted tariffs """

import numpy as np
from numpy.linalg import matrix_power


def Expenditure(alphas, B, G, Dinp, taup, Fp, VAn, wf0, Sn, J, N):

    # [J, N] = np.shape(A)
    IA = np.zeros((J * N, J * N))
    I_F = 1 - Fp

    for n in range(N):
        IA[n * J: (n + 1) * J, n * J: (n + 1) * J] = np.kron(alphas[:, n], I_F[:, n].T).reshape(40, 40)

    Pit = Dinp/taup
    Bt = 1 - B
    BP = np.zeros(np.shape(Pit))

    for j in range(J):
        BP[j * N: (j + 1) * N, :] = np.kron(np.ones(N).reshape(N, 1), Bt[j, :]) * Pit[j * N: (j + 1) * N, :]

    NBP = np.zeros(np.shape(BP.T))

    for j in range(N):
        for n in range(N):
            NBP[j, n * J: (n + 1) * J] = BP[np.arange(n, N, J * N), j]

    NNBP = np.kron(NBP, np.ones((J, 1)))
    GG = np.kron(np.ones((1, N)), G)
    GP = GG * NNBP

    OM = np.eye(J * N, J * N) - (GP + IA)
    Vb = alphas * np.kron(np.ones((J, 1)), (wf0 * VAn).T)
    Vb = Vb.reshape(J * N, 1, order='F').copy()
    Bb = -alphas * (Sn * np.ones((1, J))).T
    Bb = Bb.reshape(J * N, 1, order='F').copy()

    temp = matrix_power(OM, -1)
    DD1 = temp.dot(Vb)
    DD2 = temp.dot(Bb)
    PQ = DD1 + DD2
    PQ = PQ.reshape(J, N, order='F').copy()

    return PQ
