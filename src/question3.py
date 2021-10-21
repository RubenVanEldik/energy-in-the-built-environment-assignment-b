#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 10:35:27 2021

@author: erik
"""
import pandas as pd  # for csv reading
import matplotlib.pyplot as plt
import model_function as mf
import plots
import numpy as np


#plt.rcParams['font.family'] = 'serif'


def plot_data(data, filename, labels):
    ax = data.plot(color=['#aa3026', '#91723c', '#85ab7b', '#915a8d'])
    ax.set_xlabel('Time [hour]')
    ax.set_ylabel('Power [kW]')
    ax.legend(labels=labels)
    plots.savefig(f'../output/{filename}')


# Import the data
group = 12
season = 'summer'

filename = f'../input/AssB_Input_Group{group}_{season}.csv'
data = pd.read_csv(filename, parse_dates=True)
data.columns = ['start', 'end', 'demand', 'pv_gen', 'price', 'emission_factor']

# Run the model
results = mf.run(data, "bottom_text")

minimal_emissions = (results.grid * results.emission_factor * 0.25).sum()


results = mf.run(data, "cost")

maximum_emissions = (results.grid * results.emission_factor * 0.25).sum()

#doing bins stuff
emission_range_step = (maximum_emissions - minimal_emissions)/10

emission_constraint = np.arange(minimal_emissions, maximum_emissions + emission_range_step, emission_range_step)

pareto_dataframe = pd.DataFrame(columns = ["cost", "emission"])

#running bins stuff
for emission_step in emission_constraint:
    results = mf.run(data, "cost", emission_step)
    cost = (results.grid * results.price * 0.25).sum()
    emission = (results.grid * results.emission_factor * 0.25).sum()
    pareto_dataframe.loc[emission_step] = [cost, emission]

pareto_dataframe.plot(kind = "scatter", x="emission", y="cost")

# Plot the results input data


# Plot the results
