import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

input_directory = 'S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Case Outputs\comb_outputs_20180629_1534 Draft Initial Scenarios'
output_directory = 'S:\E3 Projects\CEC Future of Nat Gas\PATHWAYS Model\Output Tools and Charts\python'
fmt = 'png'
cases = ['FONG High Electrification', 'FONG No Building Electrification', 'FONG No Building Electrification B']

outputs_path = output_directory

varname = 'Installed_Capacity_1'

gen_list = ['CHP', 'Coal', 'Natural Gas', 'Imports', 'Nuclear', 'Hydro',
            'Biomass', 'Geothermal', 'Wind', 'Rooftop PV', 'Solar', 'Storage']

scaling = 0.001
yrange =  [0, 400] #None #[0, 800]
ylabel = 'Installed Capacity (GW)'

gen_color_dict = {
    'CHP': 'grey',
    'Coal': 'darkgrey',
    'Natural Gas': 'silver',
    'Imports': '#d9d9d9',
    'Nuclear': '#bebada',
    'Hydro': '#80b1d3',
    'Biomass': 'blue',
    'Geothermal': 'red',
    'Wind': '#8dd3c7',
    'Rooftop PV': '#fdb462',
    'Solar': '#fed976',
    'Storage': 'purple'  # 'dodgerblue',

    # 'Imported Nuclear': 'goldenrod',
    # 'Imported Coal': 'slategrey'
}

for case in cases:
    invar = pd.read_csv(os.path.join(input_directory, varname + '.csv'))
    var = invar[invar.Active_Cases == case]

    pivot = pd.crosstab(var['Output_Year'], var['Gen_Categories_w'], values=var['Value'], aggfunc=np.sum)
    pivot[np.isnan(pivot)] = 0.
    gen = pivot[gen_list]

    gen = gen.applymap(lambda x: 0 if x < 0 else x * scaling)

    fig, ax = plt.subplots()  ## this is the most flexible approach to access the mpl api
    ## can easily do subplots this way
    # plt.figure()

    gen.plot.area(ax=ax, fontsize=11,
                  color=[gen_color_dict[x] for x in gen.columns.values])  ## list comprehension using color dict above
    # plt.stackplot(gen.index, gen.values.transpose())

    if yrange is not None:
        ax.set_ylim(yrange)
    # plt.ylim(yrange)

    ax.set_ylabel(ylabel)
    # plt.ylabel(ylabel)

    ax.set_xlim([2015, 2050])

    ax.set_xlabel('')

    handles, labels = ax.get_legend_handles_labels()  ## get legend labels and boxes as variables
    lgd = ax.legend(handles=handles[::-1], labels=labels[::-1], bbox_to_anchor=[1, 1])  ## reverse order
    ## bbox moves the legend in more precise fashion
    # plt.legend(gen.columns, loc='upper left', bbox_to_anchor = [1, 1])

    ax.set_title(case, fontsize=14)
    # plt.title(case)

    ## I usually save as a png 
    ## the legend will be cut off unless use do the bbox extra artists 

    plt.savefig(outputs_path + '//' + varname + '_' + case + '.' + fmt,
                dpi=600, transparent=True, bbox_extra_artists=(lgd,),
                bbox_inches='tight', format=fmt)
    # plt.savefig(os.path.join(output_directory, varname + ', '  + case + '.' + fmt), format=fmt,
    #             )

    #plt.show()
