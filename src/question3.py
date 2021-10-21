#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 10:35:27 2021

@author: erik
"""
import pandas as pd  # for csv reading
import model_function as mf
import plots
import numpy as np


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

# Run the model for cost optimization
cost_results = mf.run(data, 'emissions')
minimal_emissions = (cost_results.grid *
                     cost_results.emission_factor * 0.25).sum()

# Run the model for emissions optimization
em_results = mf.run(data, 'cost')
maximum_emissions = (em_results.grid * em_results.emission_factor * 0.25).sum()

# Calculate the steps for the Pareto frontier
width = (maximum_emissions - minimal_emissions) / 10
emissions_steps = np.arange(
    minimal_emissions, maximum_emissions + width, width)

# Create the Pareto frontier
pareto_dataframe = pd.DataFrame(columns=['cost', 'emissions'])
for max_emissions in emissions_steps:
    results = mf.run(data, 'cost', max_emissions)
    cost = (results.grid * results.price * 0.25).sum()
    emission = (results.grid * results.emission_factor * 0.25).sum()
    pareto_dataframe.loc[max_emissions] = [cost, emission]

pareto_dataframe.plot(kind='scatter', x='emissions', y='cost')
