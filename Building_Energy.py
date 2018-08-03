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

fmt = 'png'
cases = ['FONG High Electrification', 'FONG No Bldg Elect with Gas HPs', 'FONG No Building Electrification with SNG']

varnames = ['Final_Ene_Dem_Ext_O']

other_key = 'Other'
keys = ['Electricity', 'Biomethane', 'Natural Gas', 'Hydrogen', 'Power to Gas', other_key]

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
    # yrange_in = yrange[i]
    data = []
    for case in cases:
        pivot = plot_util.stacked_area(invar, case, varname, output_directory, index_name=index_name, fmt=fmt,
                                       keys=keys,
                                       other_key=other_key,
                                       labels_dict=labels_dict,
                                       color_dict=color_dict,
                                       scaling=scaling_in, ylabel=ylabel_in,
                                       time_index=time_index_in, select=select)
        data.append(pivot)
