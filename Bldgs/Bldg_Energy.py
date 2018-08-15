import pandas as pd
import numpy as np
import os
import matplotlib as mpl
from matplotlib import pyplot as plt
import itertools
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
import plot_util

fontsize = 12

fmt = 'png'

kwh_to_mmbtu = 3.6 / 1000 / 1.055
kbtu_to_mmbtu = 1.e-3

# print(plot_util.ETHREE_COL)


index_names = ['Climate Zone', 'Home Type', 'Vintage', 'Home Fuel']
ylim = [0, 100]

input_directory = r'S:\E3 Projects\SCE Building Electrification\Building Simulations\building_simulation_inputs_8-14-18'
output_directory = r'S:\E3 Projects\SCE Building Electrification\Building Simulations\Result Figures\Total Energy'

cz_str = ['CZ03', 'CZ04', 'CZ06', 'CZ09', 'CZ10', 'CZ12']
hy_str = ['SFH', ]

vt_str = ['1400', '2100', '2700']
fuel_str = ['Mixed', 'All-Electric']
fuel_dict = {'Mixed': '1gas',
             'All-Electric': '2electric'}
fuel_types = ['Electric (Mixed)', 'Gas (Mixed)', 'All-Electric']
fuel_lookup = {'Electric (Mixed)': 'Total Electricity [kWh]',
               'Gas (Mixed)': 'Total Gas [kBtu]',
               'All-Electric': 'Total Electricity [kWh]'}
scaling = {'Electric (Mixed)': kwh_to_mmbtu,
           'Gas (Mixed)': kbtu_to_mmbtu,
           'All-Electric': kwh_to_mmbtu}

vt_dict = {
    '1400': 'Pre-1978',
    '2100': '1990s',
    '2700': 'New'
}

ele_util_dict = {
    'CZ03': ['PG&E', ],
    'CZ04': ['PG&E', ],
    'CZ12': ['SMUD', ],
    'CZ06': ['SCE', 'LADWP', 'LADWPT1'],
    'CZ09': ['SCE', ],
    'CZ10': ['SCE', ],
}

'''
util_trans = {
    'PG&E': 'PG&E-TOU',
    'SMUD': 'SMUD-TOU',
    'SCE': 'SCE-TOU',
    'LADWP': 'LADWP-TOU',
    'LADWPT1': 'LADWP-Tiered',
    'LADWPT2': 'LADWP-Tiered',
}

#Define colors for each scenario
std_colors = {
    'ac': (0.59607843137254901, 0.55686274509803924, 0.83529411764705885, 1.0), 
    'hvac': (0.46666666666666667, 0.46666666666666667, 0.46666666666666667, 1.0), 
    'appliance': (0.98431372549019602, 0.75686274509803919, 0.36862745098039218, 1.0), 
    'wh': (0.88627450980392153, 0.29019607843137257, 0.20000000000000001, 1.0), 
    'sh': (0.20392156862745098, 0.54117647058823526, 0.74117647058823533, 1.0), 
    'allele': (0.55686274509803924, 0.72941176470588232, 0.25882352941176473, 1.0)
}

ann_ele_sav_df = pd.DataFrame()
ann_gas_sav_df = pd.DataFrame()
'''

data = pd.DataFrame(
    index=pd.MultiIndex.from_product([cz_str, hy_str, vt_str, [fuel_dict[x] for x in fuel_str]], names=index_names),
    columns=fuel_types)

for idx in data.index.tolist():
    print(idx)
    vt = idx[2]
    hy = idx[1]
    cz = idx[0]
    fuel = idx[3]
    sce_nm = vt + '_' + cz + '_' + fuel
    print(sce_nm)
    inputfile = os.path.join(input_directory, sce_nm + '.csv')

    df = pd.read_csv(inputfile, index_col=0)

    for fl in fuel_types:
        if (fl == 'All-Electric' and fuel == fuel_dict['Mixed']) or (
                fl == 'Electric (Mixed)' and fuel == fuel_dict['All-Electric']):
            data.loc[idx, fl] = 0.
        else:
            data.loc[idx, fl] = df[fuel_lookup[fl]].sum() * scaling[fl]

group_size = 2
num_series = len(vt_str) * len(fuel_str)
# Plot!
for cz, hy in itertools.product(cz_str, hy_str):
    df = data.loc[cz, hy]
    ax = df.plot.bar(stacked=True, rot=0, color=[plot_util.ETHREE_COL[x] for x in [1, 0, 1]], fontsize=fontsize)
    ax.set_xticks(range(0, len(df.index), 2))
    ax.set_xticklabels([vt_dict[x] for x in df.index.levels[0].tolist()], fontsize=fontsize)
    ax.set_xlabel('')
    ax.set_title(cz + ' ' + hy, fontsize=fontsize + 3)
    # set yaxis label
    ax.set_ylabel('Total Annual Energy (MMBtu)', fontsize=fontsize)
    ax.set_ylim(ylim)

    ax = plot_util.shade(ax, group_size, num_series)

    bars = ax.patches
    patterns = [' ', ] * 2 * num_series + ['///', ] * num_series
    for bar, pattern in zip(bars, patterns):
        bar.set_hatch(pattern)

    plt.legend(fontsize=fontsize)

    plt.savefig(os.path.join(output_directory, cz + ' ' + hy + '.' + fmt), format=fmt)
