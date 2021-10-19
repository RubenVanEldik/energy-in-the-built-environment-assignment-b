import pandas as pd  # for csv reading
import matplotlib.pyplot as plt  # for plotting
import model


"""
Import your input data for the model
"""
group = 10
season = 'summer'

filename = f'../input/AssB_Input_Group{group}_{season}.csv'
data = pd.read_csv(filename, parse_dates=True)
data.columns = ['start', 'end', 'demand', 'pv_gen', 'price', 'emission_factor']

# Run the model
results = model.run(data)


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
