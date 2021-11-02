import numpy as np
import matplotlib.pyplot as plt
import model_function as mf
import plots


plt.rcParams['font.family'] = 'serif'


def initiate_figure(*, xlabel='Time [hour]', ylabel='Power [kW]'):
    # Create a figure
    figure, axes = plots.create_plot_with_subplots(
        2, 1, xlabel=xlabel, ylabel=ylabel)
    return figure, axes


def initiate_subplot(axes, index, season):
    subplot = axes[index]
    subplot.title.set_text(season)
    labels = ['0:00', '12:00', '0:00', '12:00', '0:00', '12:00', '00:00']
    plt.xticks(np.arange(289, step=48), labels)
    return subplot


# Set the group and seasons
group = 12
seasons = ['Summer', 'Winter']

# Run the model for each season
results = {}
for index, season in enumerate(seasons):
    # Create the Pareto frontier for both the line and scatter plot
    result = mf.run(group, season, 'emissions')

    cost = (result.grid * result.price * 0.25).sum()
    print('Optimised cost for {} is €{:.2f}'.format(season.lower(), cost))
    results[season] = result


# Create a plot with the demand and PV generation
figure, axes = initiate_figure()
for index, season in enumerate(results):
    subplot = initiate_subplot(axes, index, season)
    subplot.plot(results[season].demand, color='#aa3026', label='Demand')
    subplot.plot(results[season].pv_gen, color='#91723c', label='PV')

    if index == 0:
        subplot.legend(bbox_to_anchor=(1, 1), loc='upper left')
plots.savefig('../output/demand_and_pv.png')

# Create a plot with the price and state of charge
figure, axes = initiate_figure(ylabel='Battery power [kW]')
for index, season in enumerate(results):
    subplot = initiate_subplot(axes, index, season)
    subplot2 = subplot.twinx()
    subplot2.set_ylabel('Electricity price [€/kWh]')

    plot1 = subplot.plot(results[season].battery_power,
                         color='#aa3026', label='Battery power')
    plot2 = subplot2.plot(results[season].price, color='#91723c',
                          label='Electricity price')

    if index == 0:
        allplots = plot1 + plot2
        labels = [plot.get_label() for plot in allplots]
        subplot.legend(allplots, labels, bbox_to_anchor=(
            1.12, 1), loc='upper left')
plots.savefig('../output/price_vs_battery.png')

# Create a plot with all power flows
figure, axes = initiate_figure()
for index, season in enumerate(results):
    subplot = initiate_subplot(axes, index, season)
    subplot.plot(results[season].grid, color='#aa3026', label='Grid')
    subplot.plot(results[season].battery_power,
                 color='#91723c', label='Battery')
    if index == 0:
        subplot.legend(bbox_to_anchor=(1, 1), loc='upper left')
plots.savefig('../output/power_flows.png')
