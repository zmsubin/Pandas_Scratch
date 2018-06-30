import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

input_directory = 'S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180629_1534 Draft Initial Scenarios'
output_directory = 'S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python'
fmt = 'pdf'
cases = ['FONG High Electrification', 'FONG No Building Electrification']

varname = 'Annual_Energy_Balanc'

gen_list = ['CHP', 'Coal', 'Imported Coal', 'Gas', 'Imported Gas', 'Imported BPA', 'Nuclear', 'Imported Nuclear', 'Large Hydro',
            'Other Renewables', 'Wind', 'Distributed PV', 'Utility PV', 'Curtailment']

for case in cases:

    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'))
    var = invar[invar.Active_Cases == case]

    print(var)

    pivot = pd.crosstab(var['Output_Year'], var['Energy_Balance_Index'], values=var['Value'], aggfunc=np.sum)
    pivot[np.isnan(pivot)] = 0.
    gen = pivot[gen_list]

    print(gen)

    plt.figure()
    plt.stackplot(gen.index, gen.values.transpose())
    plt.ylim([0, 800])
    plt.legend(gen.columns, loc='upper left')
    plt.title(case)

    plt.savefig(os.path.join(output_directory, varname + ', '  + case + '.' + fmt), format=fmt)