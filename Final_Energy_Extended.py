import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import plot_util

input_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180731_1440"
output_directory = r"S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python\Final Energy Extended"

try:
    os.mkdir(output_directory)
except OSError:
    pass

fmt = 'png'
# cases = ['FONG High Electrification', 'FONG No Building Electrification with SNG', 'FONG No Bldg Elect with Gas HPs',
#          'FONG No Bldg Elect with Industry & Truck Measures', 'Current Policy Reference']
# xlabels = ['High\nElectrification', 'No Building\nElectrification', 'No Building\nElectrification\nwith Gas HPs',
#            'No Bldg. Elect.\nwith Industry\n& Truck Measures', 'Current\nPolicy']
cases = ['FONG Medium Building Electrification', 'FONG Medium Buildings Branching High',
         'FONG Medium Buildings Branching Low']
xlabels = ['Hybrid', 'Hybrid-High', 'Hybrid-Low']

other_key = 'Other'

keys = ['Electricity',
        'Hydrogen',
        'Conventional Gasoline & Ethanol',
        'Renewable Gasoline',
        'Conventional Diesel',
        'Renewable Diesel',
        'Conventional Jet Fuel',
        'Renewable Jet Fuel',
        'Natural Gas',
        'Biomethane',
        'Synthetic Natural Gas',
        other_key
        ]

labels_dict = {'Electricity': 'Electricity',
               'Hydrogen': 'Hydrogen',
               'Conventional Gasoline / Conventional Ethanol': 'Conventional Gasoline & Ethanol',
               'Renewable Gasoline': 'Renewable Gasoline',
               'Renewable Ethanol': 'Renewable Gasoline',
               'Conventional Diesel': 'Conventional Diesel',
               'Conventional Jet Fuel': 'Conventional Jet Fuel',
               'Renewable Diesel': 'Renewable Diesel',
               'Biodiesel': 'Renewable Diesel',
               'Renewable Jet Fuel': 'Renewable Jet Fuel',
               'Natural Gas': 'Natural Gas',
               'Biogas': 'Biomethane',
               'Power to Gas': 'Synthetic Natural Gas'
               }

color_dict = {'Electricity': 'skyblue',
              'Hydrogen': 'gold',
              'Conventional Gasoline & Ethanol': 'maroon',
              'Renewable Gasoline': 'salmon',
              'Conventional Diesel': 'saddlebrown',
              'Renewable Diesel': 'sandybrown',
              'Conventional Jet Fuel': 'purple',
              'Renewable Jet Fuel': 'violet',
              'Natural Gas': 'darkgreen',
              'Biomethane': 'limegreen',
              'Synthetic Natural Gas': 'olive',
              other_key: 'black'
              }

# color_dict = {
#     'Efficient MDV Gasoline': 'lightgrey',
#     'Efficient MDV Diesel': 'grey',
#     'Diesel Hybrid MDV': 'darkgrey',
#     'MDV CNG': 'lightblue',
#     'MDV Battery Electric': 'blue',
#     'MDV Hydrogen FCV': 'darkblue'
# }

fontsize = 12  # 10

outputs_path = output_directory

varname = 'Final_Ene_Dem_Ext_O'

scaling = 1 / 1.055  # EJ to Quad
ylabel = 'Quadrillion BTU'
index_name = 'Final_Energy_Categor'
year = 2050
title = 'Final Energy Consumption in ' + str(year)
base_case = None  # 'Current Policy Reference'
filename = 'Final_Energy_Consumption_Hybrid_Cases' # 'Final_Energy_Consumption_Bookend_Cases' #'Final_Energy_Consumption_Hybrid_Cases'

invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'), na_values='NAN')
plot_util.stacked_bar(invar, year, varname, output_directory, index_name, fmt=fmt, xkeys=cases, ykeys=keys,
                      scaling=scaling, ylabel=ylabel, title=title, xlabels=xlabels, base_case=base_case,
                      fontsize=fontsize, other_key=other_key, color_dict=color_dict,
                      labels_dict=labels_dict, filename=filename)
