import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\Building Energy"
fontsize = 12

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'png'
cases = ['FONG High Electrification', 'FONG No Building Electrification with SNG']
casenames = ['High Electrification', 'No Building Electrification']

varname = 'Final_Energy1'

scaling = [100, 1000 / 1.055]  # EJ to TBTU
ylabel = ['% of Building Energy', 'TBTU']
index_name = 'Final_Energy'
select_index = 'End_Use_Sectors'
#select = ['Residential', 'Commercial']
ylim = [[0, 100], [0, 1800]]
title = ['Percent of Economywide Final Energy that is Electricity', 'Economywide Non-Electric Gas Demand']
reverse = [False, True]

time_index = 'Output_Year'

invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
value_name = 'Value'
case_index = 'Active_Cases'
xlabel = 'Year'

pivot = invar.pivot_table(index=[select_index, index_name, time_index], columns=case_index, values=value_name, aggfunc=np.sum)
var = pivot[cases]

var = var.groupby([index_name, time_index]).sum() #var.loc[select].groupby([index_name, time_index]).sum()

electric_fraction = var.loc['Electricity'] / var.groupby(time_index).sum()
gas_demand = var.loc['Pipeline Gas']

i = 0
for target in [electric_fraction, gas_demand]:
    if reverse[i]:
        target = target[target.columns.tolist()[::-1]]
        casenames_loc = casenames[::-1]
        color_loc = plot_util.ETHREE_COL[len(casenames)-1::-1]
    else:
        casenames_loc = casenames
        color_loc = plot_util.ETHREE_COL
    target *= scaling[i]
    target.plot.line(fontsize=fontsize, color=color_loc)
    plt.ylabel(ylabel[i], fontsize=fontsize)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylim(ylim[i])
    plt.legend(casenames_loc)
    plt.title(title[i], fontsize=fontsize)
    plt.savefig(os.path.join(output_directory, title[i] + '.' + fmt), format=fmt)
    i += 1