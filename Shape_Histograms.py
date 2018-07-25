import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
fmt = 'jpg'

input_directory = r'S:\ZacharySubins_Documents\PATHWAYS General'
output_directory = os.path.join(input_directory, 'Shape Histograms')
inputfile = os.path.join(input_directory, 'PATHWAYS Realized High Electrification Pre-Flexibility 2050 Load Shapes.csv')
subsectors = ['Residential Water Heating', 'Residential Space Heating', 'Commercial Water Heating', 'Commercial Space Heating']
scaling = 8760
bins = 30

df = pd.read_csv(inputfile, index_col=[0, 1])
try:
    os.mkdir(output_directory)
except OSError:
    pass

shapes = df / df.sum() * scaling

hist = []
for subsector in shapes.columns: # subsectors:
    plt.figure()
    hist.append(shapes[subsector].hist(grid=False, bins=bins))
    plt.xlabel('Normalized Load')
    plt.ylabel('# of Hours')
    plt.title(subsector)
    plt.savefig(os.path.join(output_directory, subsector + '_Extra Bins' + '.' + fmt), format=fmt)