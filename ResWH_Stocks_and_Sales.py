import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\ResWH Stocks and Sales"

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'png'
#cases = ['FONG High Electrification', 'FONG Medium Building Electrification', 'FONG No Bldg Elect with Industry & Truck Measures']

outputs_path = output_directory

varnames = ['RES_WH_Collapse', 'RES_WH_Sales_Share']

color_dict = {
    'Reference LPG WH': 'lightgrey',
    'Reference Gas WH': 'grey',
    'High Efficiency Gas WH': 'black',
    'High Efficiency LPG WH': 'brown',
    #'High Efficiency Distillate WH': 'brown',
    'Reference Electric WH': 'lightblue',
    'Heat Pump Electric WH': 'blue',
    'Gas Heat Pump WH': 'yellow'
}
exclude = 'High Efficiency Distillate WH'

keys = list(color_dict.keys())

scaling = [1e-6, 100]
yrange = [[0, 20], [0, 100]]
ylabel = ['Million Water Heaters', '% of Sales']
index_name = 'In_Use_Techs_RES_WH'

time_index = ['Year', 'Vintage']

#Pull All Cases
invar = pd.read_csv(os.path.join(input_directory, varnames[0] + '.csv'), na_values='NAN')
cases = invar['Active_Cases'].unique()


for i in range(len(varnames)):
    varname = varnames[i]
    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
    invar[invar[index_name] == exclude] = 0.
    scaling_in = scaling[i]
    ylabel_in = ylabel[i]
    time_index_in = time_index[i]
    yrange_in = yrange[i]
    for case in cases:
        plot_util.stacked_area(invar, case, varname, output_directory, index_name=index_name, fmt=fmt,
                               keys=keys,
                               color_dict=color_dict, scaling=scaling_in, yrange=yrange_in, ylabel=ylabel_in,
                               time_index=time_index_in)
