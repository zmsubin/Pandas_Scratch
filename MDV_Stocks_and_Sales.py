import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python"
fmt = 'jpg'
cases = ['FONG High Electrification', 'FONG Medium Building Electrification', 'FONG No Bldg Elect with Industry & Truck Measures']

outputs_path = output_directory

varnames = ['MDV_Collapsed', 'Sales_Share_TRA_MD']

keys = ['Efficient MDV Gasoline', 'Efficient MDV Diesel', 'Diesel Hybrid MDV', 'MDV CNG', 'MDV Battery Electric',
        'MDV Hydrogen FCV']

labels_dict = {
    'Efficient MDV Gasoline': 'Gasoline ICE',
    'Efficient MDV Diesel': 'Diesel ICE',
    'Diesel Hybrid MDV': 'Hybrid Diesel',
    'MDV CNG': 'CNG ICE',
    'MDV Battery Electric': 'BEV',
    'MDV Hydrogen FCV': 'Hydrogen FCV'
}

color_dict = {
    'Efficient MDV Gasoline': 'lightgrey',
    'Efficient MDV Diesel': 'grey',
    'Diesel Hybrid MDV': 'darkgrey',
    'MDV CNG': 'lightblue',
    'MDV Battery Electric': 'blue',
    'MDV Hydrogen FCV': 'darkblue'
}

scaling = [1e-3, 100]  # 0.001
yrange = [None, [0, 100]]  # [0, 400] #None #[0, 800]
ylabel = ['Thousand Vehicles', '% of Sales']
index_name = 'In_Use_Techs_TRA_MD'

time_index = ['Year', 'Vintage']

for i in range(len(varnames)):
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
