import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180806_1319"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\GHGs Multi-Prong"

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'png'
# cases = ['FONG High Electrification', 'FONG No Building Electrification with SNG', 'FONG No Bldg Elect with Gas HPs',
#          'FONG No Bldg Elect with Industry & Truck Measures']
# xlabels = ['High\nElectrification', 'No Building\nElectrification\nwith High SNG', 'No Building\nElectrification\nwith Gas HPs',
#            'No Bldg. Elect.\nwith Industry &\nTruck Measures']
cases = ['FONG High Electrification', 'FONG Medium Buildings Branching High', 'FONG Medium Building Electrification',  'FONG Medium Buildings Branching Low', 'FONG No Building Electrification with SNG']
xlabels = ['High\nElectrification', 'Delayed\nElectrification', 'Slower\nElectrification', 'Mixed with\nGas HPs', 'No Building\nElectrification\nwith High SNG']

other_key = 'Other Sectors'
keys = ['Electricity', 'Buildings', 'Transportation', 'Industrial', other_key]

labels_dict = {'Electric Power': 'Electricity',
               'Residential and Commercial': 'Buildings',
               'Transportation (Incl. TCU)': 'Transportation'
               }

fontsize = 12 #10

outputs_path = output_directory

varname = 'Total_Emissions_by_A'

scaling = 1  # 2012$ to $2018B
ylabel = 'MMT CO$_2$e'
index_name = 'ARB_Sectors'
year = 2050
title = 'Economywide GHG Emissions in ' + str(year)
#base_case = 'Current Policy Reference'

invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
plot_util.stacked_bar(invar, year, varname, output_directory, index_name, fmt=fmt, xkeys=cases, ykeys=keys, labels_dict=labels_dict,
                      scaling=scaling, ylabel=ylabel, title=title, xlabels=xlabels, other_key=other_key, fontsize=fontsize)
