import numpy as np
import matplotlib.pyplot as plt
import os

output_directory = 'S:\ZacharySubins_Documents\Projects\Building Electrification Market Assessment\Efficiency Analysis'
fmt = 'pdf'

eff = np.arange(2, 5, 0.1) # COP
rate = np.arange(0.05, 0.3, 0.01) # electricity price in $/kWh
gas_price = 12 # $/mmBTU
service_demand = 20 # mmBTU/yr
gas_eff = 0.8 # COP
gas_costs = service_demand / gas_eff * gas_price # $/yr
y, x = np.meshgrid(eff, rate) # x-axis is rate, y-axis is efficiency
mmbtu_per_kWh_thermal = 3.4e-3
CRF = 0.1

net_fuel_cost = service_demand / y * x / mmbtu_per_kWh_thermal - gas_costs # mmBTU / COP * $/kWh / (mmBTU/kWh)
#
# plt.figure()
#
# plt.pcolor(x, y, net_fuel_cost)
# plt.colorbar()

breakeven_cap_cost = -net_fuel_cost / CRF

plt.figure()

plt.contour(x, y, breakeven_cap_cost, cmap='coolwarm_r')
plt.colorbar()
#plt.clim([-5000, 2500])
plt.title('Breakeven Capital Cost ($)')
plt.xlabel('Electricity Rate ($/kWh)')
plt.ylabel('Heat Pump Efficiency (COP)')
plt.savefig(os.path.join(output_directory, 'Breakeven Capital Cost' + '.' + fmt), format=fmt)