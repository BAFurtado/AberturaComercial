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

    DD = np.zeros((J * N, N))
    print(Din.shape[1])
    for n in range(N):
        DD[n * N: ((n + 1) * N) - 1 : (N - 1), :] = Din_om[n: Din.shape[1] - 1 - (N - 1 - n): (N - 1), :] * cp

    phat = DD.sum(axis=1).T ** -LT

    Dinp = np.ones(1, N)
    for n in range(N):
        Dinp[:, n] = DD[:, n] * (phat ** (1/LT))

    return Dinp
