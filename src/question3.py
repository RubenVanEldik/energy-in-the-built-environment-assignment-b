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


def season_changer(group, season):
    # Run the model for cost optimization
    cost_results = mf.run(group, season, 'emissions')
    min_emissions = (cost_results.grid *
                     cost_results.emission_factor * 0.25).sum()

    # Run the model for emissions optimization
    em_results = mf.run(group, season, 'cost')
    max_emissions = (em_results.grid * em_results.emission_factor * 0.25).sum()

    # Calculate the bins for the Pareto frontier
    no_bins = 10
    bin_width = (max_emissions - min_emissions) / (no_bins - 1)
    emissions_bins = np.arange(
        min_emissions, max_emissions + bin_width, bin_width)

    # Create the Pareto frontier
    pareto_dataframe = pd.DataFrame(columns=['cost', 'emissions'])

    for index, max_emissions in enumerate(emissions_bins):
        print('\rRunning optimization {} of {}'.format(
            index + 1, len(emissions_bins)), end='')
        results = mf.run(group, season, 'cost', max_emissions)
        cost = (results.grid * results.price * 0.25).sum()
        emission = (results.grid * results.emission_factor * 0.25).sum()
        pareto_dataframe.loc[max_emissions] = [cost, emission]

    print('\r Succesfully created the Pareto frontier')
    pareto_dataframe.plot(kind='scatter', x='emissions', y='cost')


group = 12
seasons = ["summer", "winter"]
for season in seasons:
    season_changer(group, season)
