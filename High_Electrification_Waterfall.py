import waterfall_chart

measure_names = ['Reference', 'Renewables', 'LDV\nElectrification', 'Heat\nPumps', 'Other GHG\nReductions']
measure_quantities = [433, -103, -57, -27, 86.2-433+(103+57+27)]
plot = waterfall_chart.plot(measure_names, measure_quantities, rotation_value=0, figsize=(7, 4),
                            net_label='2050 Goal', Title='CA GHG Emissions in 2050', y_lab = r'MMT CO$_2$e',
                            green_color = 'red', red_color = 'green', formatting='{:,.0f}')

plot.ylim([0, 500])

plot.savefig('waterfall.pdf')