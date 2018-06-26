import numpy as np
import matplotlib.pyplot as plt
import os

output_directory = 'S:\ZacharySubins_Documents\Projects\Building Electrification Market Assessment\Efficiency Analysis'
fmt = 'pdf'

gas_prices = [12, 24] # $/mmBTU
scenario_names = ['$12 per mmBTU Gas', '$24 per mmBTU Gas']

for i in range(len(gas_prices)):

    eff = np.arange(2, 5, 0.1) # COP
    rate = np.arange(0.05, 0.3, 0.01) # electricity price in $/kWh
    gas_price = gas_prices[i] # $/mmBTU
    GJ_per_MMBTU = 1.055
    tonnes_per_GJ = 0.05 # NG emissions intensity
    gas_price += 20*tonnes_per_GJ*GJ_per_MMBTU #add CO2 price
    print('gas_price = ' + str(gas_price))
    service_demand = 20 # mmBTU/yr
    gas_eff = 0.9 # COP
    gas_costs = service_demand / gas_eff * gas_price # $/yr
    y, x = np.meshgrid(eff, rate) # x-axis is rate, y-axis is efficiency
    mmbtu_per_kWh_thermal = 3.6e-3/GJ_per_MMBTU
    COP_to_HSPF = 3.6/GJ_per_MMBTU
    CRF = -np.pmt(0.05, 15, 1)
    print('CRF = ' + str(CRF))

    net_fuel_cost = service_demand / y * x / mmbtu_per_kWh_thermal - gas_costs # mmBTU / COP * $/kWh / (mmBTU/kWh)

    breakeven_cap_cost = -net_fuel_cost / CRF

    plt.close()
    plt.figure()
    vscale = 2500
    y *= COP_to_HSPF # convert to HSPF
    plot = plt.contourf(x, y, breakeven_cap_cost, cmap='coolwarm_r', vmin=-vscale, vmax=vscale)
    #plt.clabel(plot)
    plt.colorbar()
    #plt.clim([-5000, 2500])
    plt.title('Breakeven Capital Cost Relative to Gas Furnace ($)\n' + scenario_names[i])
    plt.xlabel('Electricity Rate ($/kWh)')
    plt.ylabel('Heat Pump Efficiency (HSPF)')
    plt.savefig(os.path.join(output_directory, 'Breakeven Capital Cost, ' + scenario_names[i] + '.' + fmt), format=fmt)