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

varname = 'HDV_Collapsed'

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

scaling = 1e-3  # 0.001
yrange = None  # [0, 400] #None #[0, 800]
ylabel = 'Thousand Vehicles'
index_name = 'In_Use_Techs_TRA_HD'

invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'))
time_index = 'Year'

for case in cases:
    plot_util.stacked_area(invar, case, varname, output_directory, index_name=index_name, fmt=fmt, keys=keys,
                           labels_dict=labels_dict,
                           color_dict=color_dict, scaling=scaling, yrange=yrange, ylabel=ylabel,
                           time_index=time_index)
