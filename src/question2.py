import matplotlib.pyplot as plt
import model_function as mf
import plots


plt.rcParams['font.family'] = 'serif'


# Set the group and seasons
group = 12
seasons = ['Summer', 'Winter']

# Create two figures
xlabel = 'Time [hour]'
ylabel = 'Power [kW]'
figure, axes = plots.create_plot_with_subplots(
    2, 1, xlabel=xlabel, ylabel=ylabel)


# Create a subplot for the demand and PV for each season
for index, season in enumerate(seasons):
    # Create the Pareto frontier for both the line and scatter plot
    results = mf.run(group, season, 'emissions')

    cost = (results.grid * results.price * 0.25).sum()
    print('Optimised cost for {} season is {}'.format(season, cost))

    # Create the subplot
    subplot = axes[index]
    subplot.title.set_text(season)
    subplot.plot(results.demand, color='#aa3026')
    subplot.plot(results.pv_gen, color='#91723c')

# Save the figure
plots.savefig('../output/demand_and_pv.png')


# Create a subplot for all power flows for each season
for index, season in enumerate(seasons):
    # Create the Pareto frontier for both the line and scatter plot
    results = mf.run(group, season, 'emissions')

    cost = (results.grid * results.price * 0.25).sum()
    print('Optimised cost for {} season is {}'.format(season, cost))

    # Create the subplot
    subplot = axes[index]
    subplot.title.set_text(season)
    subplot.plot(results.demand, color='#aa3026')
    subplot.plot(results.pv_gen, color='#91723c')
    subplot.plot(results.grid, color='#85ab7b')
    subplot.plot(results.battery_power, color='#915a8d')

# Save the figure
plots.savefig('../output/power_flows.png')
