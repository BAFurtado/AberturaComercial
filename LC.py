import numpy as np

import LMC
import dinprime
import expenditure
import ph


def Equilibrium_LC(tau_hat, taup, alphas, T, B, G, Din, J, N, maxit, tol, VAn, Sn, vfactor):

    # initialize vectors of ex-post wage and price factors
    wf0 = np.ones([N, 1])
    pf0 = np.ones([J, N])
    wfmax = np.array([1.0])
    e = 1.0

    while (e <= maxit) and (wfmax.all() > tol):
        pf0, c = ph.PH(wf0, tau_hat, T, B, G, Din, J, N, maxit, tol)

        # Calculating trade shares
        Dinp = dinprime.Dinprime(Din, tau_hat, c, T, J, N)
        Dinp_om = Dinp / taup

        Fp = np.zeros((J, N))
        for j in range(J):
            Fp[j, :] = sum((Dinp[j * N: (j + 1) * N: 1, :] / taup[j * N: (j + 1) * N: 1, :]).T)

        # Expenditure matrix
        PQ = expenditure.Expenditure(alphas, B, G, Dinp, taup, Fp, VAn, wf0, Sn, J, N)

        # Iterating using LMC
        wf1 = LMC.lmc(PQ, Dinp_om, J, N, B, VAn)

        # Excess function
        ZW = (wf1 - wf0)

        PQ_vec = PQ.T.reshape(1, J * N, order='F').copy().T

        DP = np.zeros((J * N, N))
        for n in range(N):
            DP[:, n] = Dinp_om[:, n] * PQ_vec.reshape(1, J * N)

        # Exports
        LHS = sum(DP).T.reshape(N, 1)

        # calculating RHS (Imports) trade balance
        PF = PQ * Fp
        # Imports
        RHS = sum(PF).T.reshape(N, 1)

        # Excess function (trade balance)
        Snp = (RHS - LHS) + Sn
        ZW2 = -(RHS - LHS + Sn) / VAn

        # Itaration factor prices
        wf1 = wf0 * (1 - vfactor * ZW2 / wf0)

        # wfmax = sum((abs(wf1 - wf0)))
        wfmax = sum(abs(Snp))

        wfmax0 = wfmax
        wf0 = wf1

        e += 1

    return wf0, pf0, PQ, Fp, Dinp, ZW, Snp, c, DP, PF
