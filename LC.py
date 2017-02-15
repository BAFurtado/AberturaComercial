import numpy as np
import ph
import dinprime


def equilibrium_LC(tau_hat, taup, alphas, T, B, G, Din, J, N, maxit, tol, VAn, Sn, vfactor):

    # initialize vectors of ex-post wage and price factors
    wf0 = np.ones([N, 1])
    pf0 = np.ones([J, N])
    wfmax = 1
    e = 1

    while e <= maxit and wfmax > tol:
        pf0, c = ph.PH(wf0, tau_hat, T, B, G, Din, J, N, maxit, tol)

        # Calculating trade shares
        Dinp = dinprime.Dinprime(Din,tau_hat,c,T,J,N)
        Dinp_om = Dinp / taup

    return wf0, pf0, PQ, Fp, Dinp, ZW, Snp, c, DP, PF
