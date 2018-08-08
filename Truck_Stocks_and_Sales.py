import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\Truck Stocks and Sales"
fmt = 'png'
cases = ['FONG High Electrification', 'FONG Medium Building Electrification', 'FONG No Bldg Elect with Industry & Truck Measures']
titles = ['High Electrification', 'No Building Electrification with High SNG', 'No Building Electrification with Industry & Truck Measures']

outputs_path = output_directory

varnames = ['HDV_Collapsed', 'Sales_Share_TRA_HD']

keys = ['Diesel ICE', 'Hybrid Diesel', 'CNG ICE', 'BEV', 'Hydrogen FCV']

labels_dict = {
    'Efficient HDV Diesel': 'Diesel ICE',
    'Hybrid Diesel HDV': 'Hybrid Diesel',
    'Efficient HDV CNG': 'CNG ICE',
    'HDV Battery Electric': 'BEV',
    'HDV Hydrogen FCV': 'Hydrogen FCV'
}

color_dict = {
    'Diesel ICE': 'silver',
    'Hybrid Diesel': 'darkgrey',
    'CNG ICE': 'skyblue',
    'BEV': 'limegreen',
    'Hydrogen FCV': 'gold'
}

scaling = [1e-3, 100]  # 0.001
yrange = [[0, 500], [0, 100]]  # [0, 400] #None #[0, 800]
ylabel = ['Thousand Vehicles', '% of Sales']
index_name = 'In_Use_Techs_TRA_HD'

time_index = ['Year', 'Vintage']

for i in range(len(varnames)):
    varname = varnames[i]
    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
    scaling_in = scaling[i]
    ylabel_in = ylabel[i]
    time_index_in = time_index[i]
    yrange_in = yrange[i]
    j = 0
    for case in cases:
        plot_util.stacked_area(invar, case, varname, output_directory, index_name=index_name, fmt=fmt, keys=keys,
                               labels_dict=labels_dict, title=titles[j],
                               color_dict=color_dict, scaling=scaling_in, yrange=yrange_in, ylabel=ylabel_in,
                               time_index=time_index_in)
        j += 1
