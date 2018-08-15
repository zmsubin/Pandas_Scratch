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

index_names = ['Climate Zone', 'Vintage', 'Home Type', 'Home Fuel']
ylim = [0, 80]

input_directory = r'S:\E3 Projects\SCE Building Electrification\Building Simulations\building_simulation_inputs_8-14-18'
output_directory = r'S:\E3 Projects\SCE Building Electrification\Building Simulations\Result Figures\Total Energy'

cz_str = ['CZ03', 'CZ04', 'CZ06', 'CZ09', 'CZ10', 'CZ12']
hy_str = ['Single-Family Home', 'Low-Rise Multifamily', 'High-Rise Multifamily']
hy_dict = {'Single-Family Home': 'SFH', 'Low-Rise Multifamily': 'LRMF', 'High-Rise Multifamily': 'HRMF'}

vt_str = ['1978', '1990s', 'New Construction']
vt_dict = {'Single-Family Home': {'1990s': '2100', '1978': '1400', 'New Construction': '2700'},
           'Low-Rise Multifamily': {'1990s': 'MF90', '1978': 'MF70', 'New Construction': 'MFNC'},
           'High-Rise Multifamily': {'1990s': '8', '1978': '9', 'New Construction': '7'}
           }

fuel_str = ['Mixed', 'All-Electric']
fuel_dict = {'Single-Family Home': {'Mixed': '1gas', 'All-Electric': '2electric'},
             'Low-Rise Multifamily': {'Mixed': '1gas', 'All-Electric': '2electric'},
             'High-Rise Multifamily': {'Mixed': 'G', 'All-Electric': 'E'}
             }

fuel_types = ['Electric (Mixed)', 'Gas (Mixed)', 'All-Electric']
fuel_lookup = {}
fuel_lookup['Single-Family Home'] = {'Electric (Mixed)': 'Total Electricity [kWh]',
                                     'Gas (Mixed)': 'Total Gas [kBtu]',
                                     'All-Electric': 'Total Electricity [kWh]'}
fuel_lookup['Low-Rise Multifamily'] = fuel_lookup['Single-Family Home']
fuel_lookup['High-Rise Multifamily'] = {'Electric (Mixed)': 'Building Electricity [kWh]',
                                        'Gas (Mixed)': 'Building Natural Gas [kBtu]',
                                        'All-Electric': 'Building Electricity [kWh]'}

scaling = {'Electric (Mixed)': kwh_to_mmbtu,
           'Gas (Mixed)': kbtu_to_mmbtu,
           'All-Electric': kwh_to_mmbtu}

house_scaling = {'Single-Family Home': 1, 'Low-Rise Multifamily': 1, 'High-Rise Multifamily': 1 / 32}

'''
ele_util_dict = {
    'CZ03': ['PG&E', ],
    'CZ04': ['PG&E', ],
    'CZ12': ['SMUD', ],
    'CZ06': ['SCE', 'LADWP', 'LADWPT1'],
    'CZ09': ['SCE', ],
    'CZ10': ['SCE', ],
}

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
    index=pd.MultiIndex.from_product([cz_str, vt_str, hy_str, fuel_str], names=index_names),
    columns=fuel_types)

for idx in data.index.tolist():
    print(idx)
    hy = idx[2]
    vt = idx[1]
    cz = idx[0]
    fuel = idx[3]
    if hy == 'High-Rise Multifamily':
        name = fuel_dict[hy][fuel] + vt_dict[hy][vt] + '_' + cz
    else:
        name = vt_dict[hy][vt] + '_' + cz + '_' + fuel_dict[hy][fuel]
    print(name)
    inputfile = os.path.join(input_directory, name + '.csv')

    df = pd.read_csv(inputfile, index_col=0)

    for fl in fuel_types:
        if (fl == 'All-Electric' and fuel == 'Mixed') or (
                fl == 'Electric (Mixed)' and fuel == 'All-Electric'):
            data.loc[idx, fl] = 0.
        else:
            data.loc[idx, fl] = df[fuel_lookup[hy][fl]].sum() * scaling[fl] * house_scaling[hy]

data.to_csv(os.path.join(output_directory, 'Total Energy Consumption.csv'))

group_size = 2
num_series = len(hy_str) * len(fuel_str)
# Plot!
for cz, vt in itertools.product(cz_str, vt_str):
    df = data.loc[cz, vt]
    ax = df.plot.bar(stacked=True, rot=0, color=[plot_util.ETHREE_COL[x] for x in [1, 0, 1]], fontsize=fontsize)
    ax.set_xticks(range(0, len(df.index), 2))
    ax.set_xticklabels([hy_dict[x] for x in hy_str], fontsize=fontsize)
    ax.set_xlabel('')
    ax.set_title(cz + ' ' + vt, fontsize=fontsize + 3)
    # set yaxis label
    ax.set_ylabel('Total Annual Energy (MMBtu)', fontsize=fontsize)
    ax.set_ylim(ylim)

    ax = plot_util.shade(ax, group_size, num_series)

    bars = ax.patches
    patterns = [' ', ] * 2 * num_series + ['///', ] * num_series
    for bar, pattern in zip(bars, patterns):
        bar.set_hatch(pattern)

    plt.legend(fontsize=fontsize)

    plt.savefig(os.path.join(output_directory, cz + ' ' + vt + '.' + fmt), format=fmt)
