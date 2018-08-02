import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\Building Energy"

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'jpg'
cases = ['FONG High Electrification', 'FONG No Bldg Elect with Gas HPs', 'FONG No Building Electrification with SNG']

varnames = ['Final_Ene_Dem_Ext_O']

other_key = 'Other'
keys = ['Electricity', 'Biogas', 'Natural Gas', 'Hydrogen', 'Power to Gas', other_key]

labels_dict = {'Electricity': 'Electricity',
               'Biogas': 'Biomethane',
               'Natural Gas': 'Natural Gas',
               'Hydrogen': 'Pipeline Hydrogen',
               'Power to Gas': 'SNG',
               other_key: other_key}

color_dict = {}
i = 0
for key in keys:
    color_dict[key] = plot_util.ETHREE_COL[i]
    i += 1

#
# color_dict = {
#     'Efficient HDV Diesel': 'grey',
#     'Hybrid Diesel HDV': 'darkgrey',
#     'Efficient HDV CNG': 'lightblue',
#     'HDV Battery Electric': 'blue',
#     'HDV Hydrogen FCV': 'darkblue'
# }

scaling = [1000 / 1.055]  # EJ to TBTU
ylabel = ['TBTU']
index_name = 'Final_Energy_Categor'
select = {'End_Use_Sectors': ['Residential', 'Commercial']}

time_index = ['Output_Year']

for i in range(len(varnames)):
    varname = varnames[i]
    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
    scaling_in = scaling[i]
    ylabel_in = ylabel[i]
    time_index_in = time_index[i]
    #yrange_in = yrange[i]
    for case in cases:
        plot_util.stacked_area(invar, case, varname, output_directory, index_name=index_name, fmt=fmt, keys=keys,
                               other_key=other_key,
                               labels_dict=labels_dict,
                               color_dict=color_dict,
                               scaling=scaling_in, ylabel=ylabel_in,
                               time_index=time_index_in, select=select)
