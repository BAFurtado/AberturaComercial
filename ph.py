import numpy as np


def PH(wages_N, tau_hat, T, B, G, Din, J, N, maxit, tol):

    # reformatting theta vector
    temp = np.ones(N)
    LT = (temp * T).reshape(J * N, 1)

    # initialize vectors of ex-post wage and price factors
    wf0 = np.ndarray.copy(wages_N)
    pf0 = np.ones([J, N])

    pfmax = 1
    it = 1

    while it <= maxit and pfmax > tol:
        lw = np.log(wf0)
        lp = np.log(pf0)

        for i in range(N):
        lc[:, i] = B[:, i].dot(lw[i]) + (1 - B[:, i]) * (G(1 + (i - 1) * J:J * i,:)'*lp(:,i));



    return pf0, c