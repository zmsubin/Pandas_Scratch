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


def othermap(val, keys, other_key='Other'):
    if val in keys:
        return val
    else:
        return other_key


def stacked_area(data, case, varname, output_directory, index_name, fmt='pdf', keys=None, labels_dict=None,
                 color_dict=None, scaling=1, yrange=None, ylabel='', case_index='Active_Cases',
                 time_index='Output_Year', value_name='Value', aggfunc=np.sum, map=None, fontsize=12,
                 xlim=(2015, 2050), xlabel='', select=None, other_key=None): #select is a dictionary of lists
    print('Stacked area chart for variable: ' + varname + ', case: ' + case)

    data = data.copy()

    var = data[data[case_index] == case]

    if labels_dict is not None:
        var[index_name] = var[index_name].map(labels_dict)

    if other_key is not None:
        var[index_name] = var[index_name].map(lambda x: othermap(x, keys, other_key))

    var[value_name] = var[value_name].map(nanmap)

    print(var.head())

    if select is None:
        pivot = pd.crosstab(var[time_index], var[index_name], values=var[value_name], aggfunc=aggfunc)
    else:
        index = list(select.keys())
        index.append(time_index)
        pivot = pd.pivot_table(var, index=index, columns=index_name, values=value_name, aggfunc=aggfunc, fill_value=0.)
        idx = pd.IndexSlice
        for column in select.keys():
            pivot = pivot.loc[idx[select[column]], idx[:]]
        pivot = pivot.groupby(time_index).sum()

    print(pivot.columns.tolist())
    if keys is None:
        active_list = pivot.columns.tolist()
    else:
        active_list = keys.copy()
        for key in keys:
            if key not in pivot.columns.tolist() or max(abs(pivot[key])) == 0.:
                active_list.remove(key)

    pivot = pivot[active_list]

    if map is None:
        map = lambda x: abs(x) * scaling
    pivot = pivot.applymap(map)

    fig, ax = plt.subplots()  ## this is the most flexible approach to access the mpl api
    ## can easily do subplots this way

    if color_dict is None:
        color = ETHREE_COL
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

    lgd = ax.legend(handles=handles[::-1], labels=labels[::-1], bbox_to_anchor=[1, 1], fontsize=fontsize)  ## reverse order
    ## bbox moves the legend in more precise fashion

    ax.set_title(case, fontsize=fontsize + 2)

    plt.savefig(os.path.join(output_directory, varname + '_' + case + '.' + fmt),
                dpi=600, transparent=False, bbox_extra_artists=(lgd,),
                bbox_inches='tight', format=fmt)

    return pivot

    # plt.close()


def reshape(df, xkeys, ykeys):
    target = df
    if ykeys is not None:
        active_list_y = ykeys.copy()
        for key in ykeys:
            if key not in df.columns.tolist():
                print('Key not found: ' + key + ': removing.')
                active_list_y.remove(key)

        target = target[active_list_y]

    if xkeys is None:
       active_list = df.index.tolist()
    else:
        active_list = xkeys.copy()
        for key in xkeys:
            if key not in df.index.tolist():
                print('Key not found: ' + key + ': removing.')
                active_list.remove(key)
        target = target.loc[active_list]

    return target, active_list


def safe_dict(x, dictionary):
    try:
        y = dictionary[x]
    except KeyError:
        y = x
    return y


def stacked_bar(data, select, varname, output_directory, index_name, fmt='pdf', xkeys=None, ykeys=None, labels_dict=None,
                color_dict=None, scaling=1, yrange=None, ylabel='', case_index='Active_Cases',
                value_name='Value', aggfunc=np.sum, map=None, fontsize=12, time_index='Output_Year',
                xlabel='', title='', xlabels=None, base_case=None, other_key=None, filename=None):

    print('Stacked bar chart for variable: ' + varname + ', year: ' + str(select))

    data = data.copy()

    #var = data[data[time_index] == select]
    var = data
    var[value_name].map(nanmap)

    if labels_dict is not None:
        var[index_name] = var[index_name].map(lambda x: safe_dict(x, labels_dict))

    if other_key is not None:
        var[index_name] = var[index_name].map(lambda x: othermap(x, ykeys, other_key))

    pivot = var.pivot_table(index=[time_index, case_index], columns=index_name, values=value_name, aggfunc=aggfunc)
    columns = pivot.columns.tolist()
    print(columns)
    cases = list(pivot.index.levels[1])
    print(cases)
    pivot = pivot.loc[select]

    target, active_list = reshape(pivot, xkeys, ykeys)

    if base_case is not None:
        for case in active_list:
            target.loc[case] = target.loc[case].subtract(pivot.loc[base_case], fill_value=0.)

    if map is None:
        map = lambda x: abs(x) * scaling
    target = target.applymap(map)

    fig, ax = plt.subplots()  ## this is the most flexible approach to access the mpl api
    ## can easily do subplots this way

    if color_dict is None:
        color = ETHREE_COL
    else:
        color = [color_dict[x] for x in target.columns.values]

    target.plot.bar(ax=ax, fontsize=fontsize, color=color, stacked=True)  ## list comprehension using color dict above

    if yrange is not None:
        ax.set_ylim(yrange)

    ax.set_ylabel(ylabel, fontsize=fontsize)

    ax.set_xlabel(xlabel, fontsize=fontsize)

    if xlabels is not None:
        if max([len(x) for x in xlabels]) > 15 and fontsize is not None:
            xlfontsize = fontsize - 3
        else:
            xlfontsize = fontsize
        ax.set_xticklabels(xlabels, rotation=0, fontsize=xlfontsize)

    handles, labels = ax.get_legend_handles_labels()  ## get legend labels and boxes as variables
    # if labels_dict is not None:
    #     labels = [labels_dict[x] for x in active_list_y]
    lgd = ax.legend(handles=handles[::-1], labels=labels[::-1], bbox_to_anchor=[1, 1], fontsize=fontsize)  ## reverse order
    ## bbox moves the legend in more precise fashion

    ax.set_title(title, fontsize=fontsize + 2)

    if filename is None:
        filename = title + '_' + str(select) + '.' + fmt
    else:
        filename += '.' + fmt

    plt.savefig(os.path.join(output_directory, filename),
                dpi=600, transparent=False, bbox_extra_artists=(lgd,),
                bbox_inches='tight', format=fmt)
