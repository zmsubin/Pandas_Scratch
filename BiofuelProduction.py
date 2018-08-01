import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\Biofuels"

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'jpg'
cases = ['FONG High Electrification', 'FONG No Building Electrification with SNG',
         'FONG No Bldg Elect with Industry & Truck Measures']
xlabels = ['High\nElectrification', 'No Building\nElectrification\nwith SNG',
           'No Bldg. Elect.\nwith Industry\n& Truck Measures']
ykeys = ['Pipeline Gas', 'Diesel', 'Gasoline', 'Jet Fuel (Kerosene)']

labels_dict = {
    'Jet Fuel (Kerosene)': 'Renewable Jet Fuel', 'Gasoline': 'Renewable Gasoline and Ethanol',
    'Diesel': 'Renewable Diesel', 'Pipeline Gas': 'Biomethane'
}

outputs_path = output_directory

varnames = ['Annual_Biofuel_Produ']

scaling = [1000 / 1.055]  # EJ to TBTU
ylabel = ['TBTU']
index_name = 'Final_Biofuels'
year = 2050
title = 'Biofuel Production in ' + str(year)

for i in range(len(varnames)):
    varname = varnames[i]
    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
    scaling_in = scaling[i]
    ylabel_in = ylabel[i]
    plot_util.stacked_bar(invar, year, varname, output_directory, index_name, fmt=fmt, xkeys=cases, ykeys=ykeys,
                          scaling=scaling_in, ylabel=ylabel_in, title=title, xlabels=xlabels, labels_dict=labels_dict)
