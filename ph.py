import numpy as np


def PH(wages_N, tau_hat, T, B, G, Din, J, N, maxit, tol):

    # reformatting theta vector
    LT = np.ones(J * N).reshape(J * N, 1)
    for j in range(J):
        for n in range(N):
            LT[j * N + n, :] = T[j, :]

    # initialize vectors of ex-post wage and price factors
    wf0 = np.ndarray.copy(wages_N)
    pf0 = np.ones([J, N])

    pfmax = 1
    it = 1

    lc = np.ones([J, N])
    Din_om = np.zeros([J * N, N])

    while it <= maxit and pfmax > tol:
        lw = np.log(wf0)
        lp = np.log(pf0)

        # calculating log cost
        for i in range(N):
            lc[:, i] = B[:, i].reshape(J, 1).dot(lw[i, :]) + (1 - B[:, i]) * G[i * J: (i + 1) * J, :].T.dot(lp[:, i])

        c = np.exp(lc)

        Din_om = Din * tau_hat ** (-1/(LT * np.ones([1, N])))

        # calculating phat
        phat = np.zeros([J, N])
        for j in range(J):
            for n in range(N):
                phat[j, n] = Din_om[j * N: (j + 1) * N, :].dot(c[j, :] ** (-1 / T[j])).T

                # this happens because of sectors with zero VA
                # Note that we do not want logs of zero
                if phat[j, n] == 0:
                    phat[j, n] = 1
                else:
                    phat[j, n] = phat[j, n] ** (-T[j])

        # Checking tolerance
        pfdev = abs(phat - pf0)
        pf0 = phat
        pfmax = max(max(pfdev))
        it += 1

    return pf0, c
