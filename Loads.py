import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\Loads"

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'png'
cases = ['FONG High Electrification', 'FONG No Building Electrification with SNG', 'FONG No Bldg Elect with Gas HPs',
         'FONG No Bldg Elect with Industry & Truck Measures', 'Current Policy Reference']
xlabels = ['High\nElectrification', 'No Building\nElectrification', 'No Building\nElectrification\nwith Gas HPs',
           'No Bldg. Elect.\nwith Industry\n& Truck Measures', 'Current\nPolicy']
ykeys = ['Ag & Other', 'Industrial', 'Buildings: Other', 'Building Electrification', 'Light-Duty Vehicles', 'Other Transportation', 'Fuel Production']

labels_dict = {'Buildings: Space Heating': 'Building Electrification',
               'Buildings: Water Heating': 'Building Electrification',
               'Buildings: Cooking and Clothes Drying': 'Building Electrification'}

fontsize= 12

outputs_path = output_directory

varnames = ['Electricity_Demand_1']

scaling = [1/1000]
ylabel = ['TWh']
index_name = 'Electricity_Load_Cat'
year = 2050
title = 'Electricity Demand in ' + str(year)

for i in range(len(varnames)):
    varname = varnames[i]
    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
    scaling_in = scaling[i]
    ylabel_in = ylabel[i]
    plot_util.stacked_bar(invar, year, varname, output_directory, index_name, fmt=fmt, xkeys=cases, ykeys=ykeys,
                          scaling=scaling_in, ylabel=ylabel_in, title=title, xlabels=xlabels, fontsize=fontsize,
                          labels_dict=labels_dict)
