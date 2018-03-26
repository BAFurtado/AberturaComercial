import numpy as np

import LMC
import dinprime
import expenditure
import ph


def Equilibrium_LC(tau_hat, taup, alphas, T, B, G, Din, J, N, maxit, tol, VAn, Sn, vfactor):

    # initialize vectors of ex-post wage and price factors
    wf0 = np.ones([N, 1])
    pf0 = np.ones([J, N])
    wfmax = 1
    e = 1

    while e <= maxit and wfmax > tol:
        pf0, c = ph.PH(wf0, tau_hat, T, B, G, Din, J, N, maxit, tol)

        # Calculating trade shares
        Dinp = dinprime.Dinprime(Din, tau_hat, c, T, J, N)
        Dinp_om = Dinp / taup

        Fp = np.zeros((1, J))
        for j in range(J):
            Fp[j, :] = sum((Dinp[j * N: 1: (j + 1) * N, :] / taup[j * N: 1: (j + 1) * N, :]).T)

        # Expenditure matrix
        PQ = expenditure.Expenditure(alphas,B,G,Dinp,taup,Fp,VAn,wf0,Sn,J,N)

        # Iterating using LMC
        wf1 = LMC.lmc(PQ, Dinp_om, J,N,B,VAn)

        # Excess function
        ZW = (wf1 - wf0)

        PQ_vec = PQ.T.reshape(1, J * N, order='F').copy().T

        DP = np.zeros((1, N))
        for n in range(N):
            DP[:, n] = Dinp_om[:, n] * PQ_vec

        # Exports
        LHS = sum(DP).T

        # calculating RHS (Imports) trade balance
        PF = PQ * Fp
        # Imports
        RHS = sum(PF).T

        # Excess function (trade balance)
        Snp = (RHS - LHS + Sn)
        ZW2 = -(RHS - LHS + Sn) / VAn

        # Itaration factor prices
        wf1 = wf0 * (1 - vfactor * ZW2 / wf0)

        wfmax = sum((abs(wf1 - wf0)))
        wfmax = sum(abs(Snp))

        wfmax0 = wfmax
        wf0 = wf1

        e += 1

    return wf0, pf0, PQ, Fp, Dinp, ZW, Snp, c, DP, PF
