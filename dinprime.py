import numpy as np


def Dinprime(Din, tau_hat, c, T, J, N):

    # reformatting theta vector
    LT = np.ones(J * N * N).reshape(J * N, N)
    for j in range(J):
        for n in range(N):
            LT[j * N + n, :] = T[j, :]

    cp = np.ones([1, N])
    for n in range(N):
        cp[:, n] = c[:, n] ** (1 / T)

    Din_om = Din * (tau_hat ** (-1 / (LT * np.ones([1, N]))))

    DD = np.ones(N, 1)
    for n in range(N):
        DD[n, :] = Din_om[n, :] * cp

    phat = sum(DD.T).T ** -LT

    Dinp = np.ones(1, N)
    for n in range(N):
        Dinp[:, n] = DD[:, n] * (phat ** (1/LT))

    return Dinp
