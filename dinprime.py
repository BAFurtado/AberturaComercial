import numpy as np


def Dinprime(Din, tau_hat, c, T, J, N):

    # reformatting theta vector
    LT = np.ones(J * N).reshape(J * N, 1)
    for j in range(J):
        for n in range(N):
            LT[j * N + n, :] = T[j, :]

    cp = np.ones(c.shape)
    for n in range(N):
        cp[:, n] = c[:, n] ** (-1 / T.reshape(1, J))

    Din_om = Din * (tau_hat ** (-1 / (LT * np.ones([1, N]))))

    DD = np.zeros((J * N, N))
    for n in range(N):
        DD[np.arange((J - 1) * n + n, J * (n + 1), 1), :] = Din_om[np.arange((J - 1) * n + n, J * (n + 1), 1), :] * cp

    phat = pow(DD.sum(axis=1).T.reshape(N * J, 1), -LT)

    Dinp = DD * (phat ** (1 / LT))

    return Dinp
