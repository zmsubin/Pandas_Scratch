import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import os

input_directory = 'S:\E3 Projects\SMUD IRP\PATHWAYS Model\Case Outputs\80 x 50 with SB 350 Biofuels Sensitivity' #'S:\E3 Projects\SMUD IRP\PATHWAYS Model\Case Outputs\comb_outputs_20180509_1039 Main 3 Scenarios'
output_directory = input_directory

cases = ['SB 350 Scenario', 'CEC No Hydrogen Low Wind SB 350 Biofuels']
geography = 'SMUD'
scaling = 1e-6

varname = 'Energy_GHGs_by_Sect1'
sectors = ['Residential', 'Commercial', 'Transportation']
fuels = ['Gasoline', 'Pipeline Gas', 'Electricity']

invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'))

pivoted = invar.pivot_table(values='Value', index=['Active_Cases', 'Geography_Energy', 'End_Use_Sectors', 'Final_Energy'], columns=['Output_Year'], aggfunc=np.sum)
pivoted *= scaling

pivoted.to_csv(os.path.join(output_directory, varname + '_Pivoted.csv'))

differences = pivoted.loc[cases[1], geography] - pivoted.loc[cases[0], geography]

idx = pd.IndexSlice
differences = differences.loc[idx[sectors, fuels], idx[:]]

differences.to_csv(os.path.join(output_directory, varname + '_Pivoted_Extracted.csv'))