# -*- coding: utf-8 -*-
"""
% Energy in the Built Environment
% Assignment 2: Optimal Home Energy Management
% Dr. Tarek AlSkaif

"""
import gurobipy as gp
import pandas as pd  # for csv reading
import matplotlib.pyplot as plt  # for plotting


"""
Import your input data for the model
"""
group = 12
season = 'summer'

filename = f'../input/AssB_Input_Group{group}_{season}.csv'
data = pd.read_csv(
    filename, parse_dates=True)
data.columns = ['start', 'end', 'demand', 'pv_gen', 'price', 'emission_factor']


"""
Parameters value
"""
# Time-step
Delta_t = 0.25  # 15 minute (0.25 hour) intervals
T = int(24*3*1/Delta_t)  # number of time-slots (in three days)

# Limits on grid and max, min, and initial SOC
Pgridmax = 3.0  # [kW]
Pbatmax = 4.0  # [kW]

SoC_min = 0.2  # [-] (battery min state of charge)
SoC_max = 1  # [-] (battery max state of charge)
SoC0 = 0.5  # [-] (initial battery state of charge at the beginning of the day)

# battery capacity parameter for a Tesla Powerwall rated at 13,5 [kWh]
C_bat = 13.5
eff_dis = 0.94  # battery discharging efficiency
eff_ch = 0.94  # battery charging efficiency

# Plot power demand and PV generation data
# f1 = plt.figure(1)


"""
Step 1: Create a model
"""

model = gp.Model('Optimising scambot 2000')


"""
Step 2: Define variables
"""
grid_power = model.addVars(data.index, lb=-Pgridmax, ub=Pgridmax)
battery_charge = model.addVars(
    data.index, lb=SoC_min * C_bat, ub=SoC_max * C_bat)
battery_power_in = model.addVars(data.index, ub=Pbatmax)
battery_power_out = model.addVars(data.index, ub=Pbatmax)


"""
Step 3: Add constraints
"""
# Power boundaries
# Power balance formula
model.addConstrs(grid_power[t] == data.demand[t]
                 - data.pv_gen[t] - battery_power_out[t]
                 + battery_power_in[t] for t in range(T))

# Battery SoC dynamics constraint
model.addConstrs(battery_charge[t] == battery_charge[t - 1] + (battery_power_in[t] *
                 Delta_t * eff_ch) - (battery_power_out[t] * Delta_t) / eff_dis for t in range(1, T))

model.addConstr(battery_power_in[0] == (
    battery_charge[0]-SoC0*C_bat)/(Delta_t*eff_ch))
model.addConstr(battery_power_out[0] == (
    (SoC0*C_bat-battery_charge[0])*eff_dis)/Delta_t)


"""
Step 4: Set objective function
"""
obj = gp.quicksum(data.price[t]*grid_power[t]*Delta_t for t in range(T))


"""
Step 5: Solve model
"""
model.setObjective(obj, gp.GRB.MINIMIZE)
model.optimize()

if model.status == gp.GRB.OPTIMAL:
    """
    Step 6: Print variables values for optimal solution
    """
    data['grid'] = model.getAttr('x', grid_power).values()
    data['battery_charge'] = model.getAttr('x', battery_charge).values()
    data['battery_in'] = model.getAttr('x', battery_power_in).values()
    data['battery_out'] = model.getAttr('x', battery_power_out).values()

    """
    Step 7: Plot optimal power output from each generator
    """
    # Plot results
    plot = data.grid.plot(kind='line')
    # data.battery_charge.plot(kind='line')
    data.battery_in.plot(kind='line')
    data.pv_gen.plot(kind='line')
    data.battery_out.plot(kind='line')
    data.demand.plot(kind='line')
    plot.legend()
