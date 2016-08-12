from read_input import np, B, GO, IO, T, tariffs1993, tariffs2005, xbilat1993, vfactor, tol, maxit, J, N

''' This is a Python 3.4.4 implementation of code made available by Caliendo and Parro, 2014 which was
    originally implemented in MatLab.
    P.S. By default, Numpy applies * form elementwise multiplication
         Matrix multiplication should use A.dot(B)

'''

# Countries = [Argentina    Australia   Austria Brazil  Canada  Chile China   Denmark Finland France...
#              Germany  Greece  Hungary India   Indonesia   Ireland Italy   Japan   Korea Mexico ...
#              Netherlands New Zealand Norway  Portugal    SouthAfrica Spain   Sweden  Turkey  UK   USA ...
#              ROW];

# Loading trade flows
# Converting into dollars from thousand dollars
xbilat1993 = xbilat1993 * 1000

# Adding the non-tradable sectors (vertically stacked, resulting matrix is shape 1240 x 31
xbilat1993_new = np.vstack((xbilat1993, np.zeros([20 * N, N])))

# Reading Tariffs
tau1993 = tariffs1993
tau2005 = tariffs2005

tau = np.vstack((1 + tau1993 / 100, np.ones([620, N])))
taup = np.vstack((1 + tau2005 / 100, np.ones([620, N])))

# For the case where there is NO CHANGE in the TARIFFS
taup = tau
# OTHERWISE, COMMENT THE ABOVE LINE

tau_hat = taup / tau

# Reading parameters
# IO Coefficients
G = IO
# Share of value added = B
# Gross output = GO
# Thetas - dispersion of productivity - non-tradables = 8.22
T = np.vstack((1 / T.reshape(20, 1), np.ones([20, 1]) * 1 / 8.22))

# Calculating expenditures
xbilat = xbilat1993_new * tau

# Domestic sales
x = np.zeros([J, N])
xbilat_domestic = xbilat / tau

for i in range(J):
    # Computing sum of partial columns (0 a 30, 31 sectors) of exports
    # Adding as rows
    x[i, :] = sum(xbilat_domestic[i * N: (i + 1) * N, :])

# Checking MAX between Exports and Domestic Product
GO = np.maximum(GO, x)
domsales = GO - x

# Bilateral trade matrix
domsales_aux = domsales.T
aux2 = np.zeros([J * N, N])

for i in range(J):
    aux2[i * N: ((i + 1) * N), :] = np.diag(domsales_aux[:, i])

xbilat = aux2 + xbilat

# Calculating X0 expenditures
A = sum(xbilat.T).reshape(1, N * J)
XO = np.zeros([40, 31])

for j in range(J):
    XO[j, :] = A[:, j * N: (j + 1) * N]

# Calculating expenditures shares
Xjn = sum(xbilat.T).T.reshape(1240,1).dot(np.ones([1,N]))
Din = xbilat / Xjn

# Calculating superavits
xbilattau = xbilat / tau
M = np.zeros([40, 31])
E = np.zeros([40, 31])
for j in range(J):
    # Imports
    M[j, :] = sum(xbilattau[j * N: (j + 1) * N,:].T).T
    for n in range(N):
        # Exports
        E[j, n] = sum(xbilattau[j * N: (j + 1) * N, n]).T

Sn = (sum(E).T - sum(M).T).reshape(N, 1)

# Calculating Value Added
VAjn = GO * B
VAn = sum(VAjn).T.reshape(N, 1)

num = np.zeros([J, N])
for n in range(N):
    num[:, n] = XO[:, n] - G[n * J:(n + 1) * J, :].dot((1 - B[:, n]) * E[:, n])

F = np.zeros([J, N])
for j in range(J):
    F[j, :] = sum((Din[j * N: (j + 1) * N, :] / tau[j * N: (j + 1) * N, :]).T)

alphas = num / (np.ones([J, 1]).dot((VAn + sum(XO * (1 - F)).T - Sn).T))

for j in range(J):
    for n in range(N):
        if alphas[j, n] < 0:
            alphas[j, n] = 0

alphas = (alphas / np.ones([J, 1])).dot(sum(alphas))

