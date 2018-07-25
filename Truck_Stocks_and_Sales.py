import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\Mitigation Scenario Truck Stocks 2018-07-02"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python"
fmt = 'png'
cases = ['FONG High Electrification', 'FONG No Building Electrification', 'FONG No Building Electrification B']

outputs_path = output_directory

varnames = ['HDV_Collapsed', 'Sales_Share_TRA_HD']

keys = ['Efficient HDV Diesel', 'Hybrid Diesel HDV', 'Efficient HDV CNG', 'HDV Battery Electric', 'HDV Hydrogen FCV']

labels_dict = {
    'Efficient HDV Diesel': 'Diesel ICE',
    'Hybrid Diesel HDV': 'Hybrid Diesel',
    'Efficient HDV CNG': 'CNG ICE',
    'HDV Battery Electric': 'BEV',
    'HDV Hydrogen FCV': 'Hydrogen FCV'
}

color_dict = {
    'Efficient HDV Diesel': 'grey',
    'Hybrid Diesel HDV': 'darkgrey',
    'Efficient HDV CNG': 'lightblue',
    'HDV Battery Electric': 'blue',
    'HDV Hydrogen FCV': 'darkblue'
}

scaling = [1e-3, 100]  # 0.001
yrange = [[0, 500], [0, 100]]  # [0, 400] #None #[0, 800]
ylabel = ['Thousand Vehicles', '% of Sales']
index_name = 'In_Use_Techs_TRA_HD'

time_index = ['Year', 'Vintage']

for i in [1]: #range(len(varnames)):
    varname = varnames[i]
    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
    scaling_in = scaling[i]
    ylabel_in = ylabel[i]
    time_index_in = time_index[i]
    yrange_in = yrange[i]
    for case in cases:
        plot_util.stacked_area(invar, case, varname, output_directory, index_name=index_name, fmt=fmt, keys=keys,
                               labels_dict=labels_dict,
                               color_dict=color_dict, scaling=scaling_in, yrange=yrange_in, ylabel=ylabel_in,
                               time_index=time_index_in)