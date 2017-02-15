# -*- coding: utf-8 -*-
import glob
import os

from scipy import io
import pandas as pd
import matplotlib.pyplot as plt

try:
    plt.style.use('ggplot')
except AttributeError:
    pass

import columns
import agg

dir = 'c:/users/r1702898/Documents/DISET/AberturaComercial/Resultados/*.*'
files = glob.glob(dir)

results = {}

for each in files:
    results[each.split('_')[2].split('.')[0]] = (io.loadmat(each))

base = results['base']
del results['base']

setores = ['agro', 'extrativa', 'industria', 'servicos']
content = [agg.agro, agg.extrativa, agg.industria, agg.servicos]

aggregated = [True, False]

for x in range(len(aggregated)):
    for graph in results['100'].keys():
        if graph[0] != '_':
            if graph == 'cresc_trab' or graph == 'Y':
                col = columns.columns + ['Desemprego']
            else:
                col = columns.columns

            if aggregated[x]:
                extra = 'agg/'
            else:
                extra = ''

            for key in results.keys():
                if aggregated[x]:
                    a = pd.DataFrame((results[key][graph] - base[graph]), columns=col)

                    for i, j in enumerate(setores):
                        a[j] = 0
                        for k in content[i]:
                            a[j] += a[k]

                    for m in a.columns:
                        if m not in setores:
                            del a[m]
                    a = a.T

                else:
                    a = pd.DataFrame((results[key][graph] - base[graph]).T, index=col)

                b = a.sort(columns=1, axis=0, ascending=False)
                fig = b.plot.bar(width=1).get_figure()
                fig.set_size_inches(18, 12)
                fig.savefig(os.path.join(dir.split('*.*')[0], 'Figuras/', extra, (graph + '_' + key)), dpi=800,
                            colormap="Spectral", bbox_inches='tight')
