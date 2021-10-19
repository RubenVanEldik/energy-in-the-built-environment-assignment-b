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
input_file = pd.read_csv(
    filename, index_col='Start date/time', parse_dates=True)
input_file.columns = ['end', 'demand', 'pv_gen', 'price', 'emission_factor']
input_file.index.names = ['start']


"""
Parameters value
"""
# Time-step
Delta_t = 0.25  # 15 minute (0.25 hour) intervals
T = 24*3*1/Delta_t  # number of time-slots (in three days)

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
f1 = plt.figure(1)


"""
Step 1: Create a model
"""

model = gp.Model('Optimising scambot 2000')

"""
Step 2: Define variables
"""
# Define your decision variables for the time horizon using addVars


grid_power = model.addVars(input_file.index, name="grid_power")

# including SoC constraints
battery_charge = model.addVars(
    input_file.index, name="battery_charge", lb=SoC_min * C_bat, ub=SoC_max * C_bat)

battery_power = model.addVars(input_file.index, name="battery_power")


"""
Step 3: Add constraints
"""
# Nonnegative variables

# Power boundaries
model.addConstrs((grid_power[t]) <= Pgridmax for t in input_file.index)
model.addConstrs(gp.abs_(battery_power[t]) <= Pbatmax for t in range(T))

# Power balance formula
model.addConstrs(grid_power[t] == input_file.demand[t] - input_file.pv_gen[t] 
                 - battery_power[t] for t in range(T))

# Battery SoC dynamics constraint
model.addConstrs(
    battery_power[t] == 
    (-(battery_charge[t]-battery_charge[t-1])/(Delta_t*eff_ch) 
     if (battery_charge[t]-battery_charge[t-1]) >= 0 
     else -((battery_charge[t]-battery_charge[t-1])*eff_dis)/(Delta_t)) 
    for t in range(T)
    )

"""
Step 4: Set objective function
"""
obj = gp.quicksum(input_file.price[t]*grid_power[t]*Delta_t for t in range(T))

"""
Step 5: Solve model
"""
model.setObjective(obj, gp.GRB.MINIMIZE)
model.optimize()

"""
Step 6: Print variables values for optimal solution
"""
# Get the values of the decision variables

"""
Step 7: Plot optimal power output from each generator 
"""
# Plot results
f2 = plt.figure(2)
