import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\Net Costs Hybrid Cases"

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'jpg'
# cases = ['FONG High Electrification', 'FONG No Building Electrification with SNG', 'FONG No Bldg Elect with Gas HPs',
#          'FONG No Bldg Elect with Industry & Truck Measures']
# xlabels = ['High\nElectrification', 'No Building\nElectrification', 'No Building\nElectrification\nwith Gas HPs',
#            'No Bldg. Elect.\nwith Industry\n& Truck Measures']
cases = ['FONG Medium Building Electrification', 'FONG Medium Buildings Branching High', 'FONG Medium Buildings Branching Low']
xlabels = ['Hybrid', 'Hybrid-High', 'Hybrid-Low']

other_key = 'Ag & Industry'
keys = ['Residential', 'Commercial', 'Transportation', other_key]
fontsize = 12 #10

outputs_path = output_directory

varname = 'Total_Costs1'

scaling = 1e-9*1.09  # 2012$ to $2018B
ylabel = 'Billion 2018$'
index_name = 'End_Use_Sectors'
year = 2050
title = 'Net Costs Relative to Current Policy in ' + str(year)
base_case = 'Current Policy Reference'

invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
plot_util.stacked_bar(invar, year, varname, output_directory, index_name, fmt=fmt, xkeys=cases, ykeys=keys,
                      scaling=scaling, ylabel=ylabel, title=title, xlabels=xlabels, base_case=base_case, other_key=other_key, fontsize=fontsize)
