import pandas as pd  # for csv reading
import matplotlib.pyplot as plt
import model_function as mf
import plots


plt.rcParams['font.family'] = 'serif'


def plot_data(data, filename, labels):
    ax = data.plot(color=['#aa3026', '#91723c', '#85ab7b', '#915a8d'])
    ax.set_xlabel('Time [hour]')
    ax.set_ylabel('Power [kW]')
    ax.legend(labels=labels)
    plots.savefig(f'../output/{filename}')

def optimum_perseason(season):
    filename = f'../input/AssB_Input_Group{group}_{season}.csv'
    data = pd.read_csv(filename, parse_dates=True)
    data.columns = ['start', 'end', 'demand', 'pv_gen', 'price', 'emission_factor']
    
    # Run the model
    results = mf.run(data)
    
    cost = (results.grid * results.price * 0.25).sum()
    print('Optimised cost for {} season is {}'.format(
            season, cost))
    
    # Plot the results input data
    data = data[['demand', 'pv_gen']]
    filename = f'demand_and_pv_{season}_{group}.png'
    legend = ['Demand', 'PV']
    plot_data(data, filename, legend)
    
    # Plot the results
    data = results[['demand', 'pv_gen', 'grid', 'battery_power']]
    filename = f'results_{season}_{group}.png'
    legend = ['Demand', 'PV', 'Grid', 'Battery']
    plot_data(data, filename, legend)

# Import the data
group = 12
seasons = ["summer", "winter"]
for season in seasons:
    optimum_perseason(season)