import numpy as np


def Dinprime(Din, tau_hat, c, T, J, N):

    # reformatting theta vector
    LT = np.ones(J * N * N).reshape(J * N, N)
    for j in range(J):
        for n in range(N):
            LT[j * N + n, :] = T[j, :]

    cp = np.ones(c.shape)
    for n in range(N):
        cp[:, n] = c[:, n] ** (-1 / T.reshape(1, J))

    Din_om = Din * (tau_hat ** (-1 / (LT * np.ones([1, N]))))

    DD = np.ones((J, N))
    for n in range(N):
        idx = N - (N - n)
        DD = Din_om[n: idx + 1: N, :] * cp

    phat = sum(DD.T).T.reshape(J, 1) ** -LT

    Dinp = np.ones(1, N)
    for n in range(N):
        Dinp[:, n] = DD[:, n] * (phat ** (1/LT))

    return Dinp
