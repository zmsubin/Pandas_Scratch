import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

ETHREE_COL = [(3 / 255, 78 / 255, 110 / 255), (175 / 255, 126 / 255, 0),
              (175 / 255, 34 / 255, 0 / 255), (0 / 255, 126 / 255, 51 / 255),
              (175 / 255, 93 / 255, 0 / 255), (10 / 255, 25 / 255, 120 / 255),
              (52 / 255, 157 / 255, 202 / 255), (255 / 255, 199 / 255, 57 / 255),
              (255 / 255, 95 / 255, 57 / 255), (48 / 255, 215 / 255, 15 / 255),
              (255 / 255, 162 / 255, 57 / 255), (68 / 255, 88 / 255, 210 / 255)
              ]


def nanmap(val, fillval=0):
    if np.isnan(val):
        return fillval
    else:
        return val


def stacked_area(data, case, varname, output_directory, index_name, fmt='pdf', keys=None, labels_dict=None,
                 color_dict=None, scaling=1, yrange=None, ylabel='', case_index='Active_Cases',
                 time_index='Output_Year', value_name='Value', aggfunc=np.sum, map=None, fontsize=12,
                 xlim=(2015, 2050), xlabel=''):
    print('Stacked area chart for variable: ' + varname + ', case: ' + case)

    data = data.copy()

    var = data[data[case_index] == case]
    var[value_name].map(nanmap)

    pivot = pd.crosstab(var[time_index], var[index_name], values=var[value_name], aggfunc=aggfunc)
    print(pivot.columns.tolist())
    if keys is None:
        active_list = pivot.columns.tolist()
    else:
        active_list = keys.copy()
        for key in keys:
            if key not in pivot.columns.tolist():
                active_list.remove(key)

    pivot = pivot[active_list]

    if map is None:
        map = lambda x: abs(x) * scaling
    pivot = pivot.applymap(map)

    fig, ax = plt.subplots()  ## this is the most flexible approach to access the mpl api
    ## can easily do subplots this way

    if color_dict is None:
        color = None
    else:
        color = [color_dict[x] for x in pivot.columns.values]

    pivot.plot.area(ax=ax, fontsize=fontsize, color=color)  ## list comprehension using color dict above
    # plt.stackplot(gen.index, gen.values.transpose())

    if yrange is not None:
        ax.set_ylim(yrange)

    ax.set_ylabel(ylabel, fontsize=fontsize)

    if xlim is not None:
        ax.set_xlim(xlim)

    ax.set_xlabel(xlabel)

    handles, labels = ax.get_legend_handles_labels()  ## get legend labels and boxes as variables
    if labels_dict is not None:
        labels = [labels_dict[x] for x in active_list]
    lgd = ax.legend(handles=handles[::-1], labels=labels[::-1], bbox_to_anchor=[1, 1])  ## reverse order
    ## bbox moves the legend in more precise fashion

    ax.set_title(case, fontsize=fontsize + 2)

    plt.savefig(os.path.join(output_directory, varname + '_' + case + '.' + fmt),
                dpi=600, transparent=True, bbox_extra_artists=(lgd,),
                bbox_inches='tight', format=fmt)

    # plt.close()


def stacked_bar(data, select, varname, output_directory, index_name, fmt='pdf', xkeys=None, ykeys=None, labels_dict=None,
                color_dict=None, scaling=1, yrange=None, ylabel='', case_index='Active_Cases',
                value_name='Value', aggfunc=np.sum, map=None, fontsize=12, time_index='Output_Year',
                xlabel='', title='', xlabels=None):
    print('Stacked bar chart for variable: ' + varname + ', year: ' + str(select))

    data = data.copy()

    var = data[data[time_index] == select]
    var[value_name].map(nanmap)

    pivot = pd.crosstab(var[case_index], var[index_name], values=var[value_name], aggfunc=aggfunc)
    print(pivot.columns.tolist())

    if ykeys is None:
        active_list_y = pivot.columns.tolist()
    else:
        active_list_y = ykeys.copy()
        for key in ykeys:
            if key not in pivot.columns.tolist():
                active_list_y.remove(key)

    pivot = pivot[active_list_y]

    if xkeys is None:
        active_list = pivot.index.tolist()
    else:
        active_list = xkeys.copy()
        for key in xkeys:
            if key not in pivot.index.tolist():
                active_list.remove(key)

    pivot = pivot.loc[active_list]

    if map is None:
        map = lambda x: abs(x) * scaling
    pivot = pivot.applymap(map)

    fig, ax = plt.subplots()  ## this is the most flexible approach to access the mpl api
    ## can easily do subplots this way

    if color_dict is None:
        color = ETHREE_COL
    else:
        color = [color_dict[x] for x in pivot.columns.values]

    pivot.plot.bar(ax=ax, fontsize=fontsize, color=color, stacked=True)  ## list comprehension using color dict above

    if yrange is not None:
        ax.set_ylim(yrange)

    ax.set_ylabel(ylabel, fontsize=fontsize)

    ax.set_xlabel(xlabel)

    if xlabels is not None:
        ax.set_xticklabels(xlabels, rotation=0)

    handles, labels = ax.get_legend_handles_labels()  ## get legend labels and boxes as variables
    if labels_dict is not None:
        labels = [labels_dict[x] for x in active_list_y]
    lgd = ax.legend(handles=handles[::-1], labels=labels[::-1], bbox_to_anchor=[1, 1])  ## reverse order
    ## bbox moves the legend in more precise fashion

    ax.set_title(title, fontsize=fontsize + 2)

    plt.savefig(os.path.join(output_directory, varname + '_' + str(select) + '.' + fmt),
                dpi=600, transparent=True, bbox_extra_artists=(lgd,),
                bbox_inches='tight', format=fmt)
