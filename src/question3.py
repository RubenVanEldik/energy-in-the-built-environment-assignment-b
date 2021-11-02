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
from matplotlib import pyplot as plt


def plot_data(data, filename, labels):
    ax = data.plot(color=['#aa3026', '#91723c', '#85ab7b', '#915a8d'])
    ax.set_xlabel('Time [hour]')
    ax.set_ylabel('Power [kW]')
    ax.legend(labels=labels)
    plots.savefig(f'../output/{filename}')


def season_changer(group, season, no_bins):
    # Run the model for cost optimization
    cost_results = mf.run(group, season, 'emissions')
    min_emissions = (cost_results.grid *
                     cost_results.emission_factor * 0.25).sum()

    # Run the model for emissions optimization
    em_results = mf.run(group, season, 'cost')
    max_emissions = (em_results.grid * em_results.emission_factor * 0.25).sum()

    # Create the Pareto frontier
    pareto_dataframe = pd.DataFrame(columns=['cost', 'emissions'])
    bins = np.linspace(min_emissions, max_emissions, num=no_bins)

    for index, max_emissions in enumerate(bins):
        print('\rRunning optimization {} of {}'.format(
            index + 1, no_bins), end='')
        results = mf.run(group, season, 'cost', max_emissions)
        cost = (results.grid * results.price * 0.25).sum()
        emission = (results.grid * results.emission_factor * 0.25).sum()
        pareto_dataframe.loc[max_emissions] = [cost, emission]

    print('\r Succesfully created the Pareto frontier')
    return pareto_dataframe


# Set the group and seasons and create a figure with two vertical plots
group = 12
seasons = ['Summer', 'Winter']

# Create a subplot for each season
for index, season in enumerate(seasons):
    # Create the Pareto frontier for both the line and scatter plot
    low_res = season_changer(group, season.lower(), 10)
    high_res = season_changer(group, season.lower(), 100)

    # Create the subplot
    plt.plot(high_res.cost, color='#aa3026', linewidth=0.8)
    plt.scatter(x=low_res.emissions, y=low_res.cost, color='#aa3026')

# Save the figure
plt.xlabel('Emissions [$kg\:CO_2$]')
plt.ylabel('Costs [$€$]')
plots.savefig('../output/pareto_frontier.png')
