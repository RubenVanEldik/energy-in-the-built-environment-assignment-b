import gurobipy as gp


def run(data, optimisation_target="cost", max_emission=None):
    data = data.copy()
    """
    Parameters value
    """
    # Time-step
    Delta_t = 0.25  # 15 minute (0.25 hour) intervals
    T = int(24*3*1/Delta_t)  # number of time-slots (in three days)

    # Limits on grid and max, min, and initial SOC
    P_grid_max = 3.0  # [kW]
    P_bat_max = 4.0  # [kW]

    SoC_min = 0.2  # [-] (battery min state of charge)
    SoC_max = 1  # [-] (battery max state of charge)
    # [-] (initial battery state of charge at the beginning of the day)
    SoC0 = 0.5

    # battery capacity parameter for a Tesla Powerwall rated at 13,5 [kWh]
    C_bat = 13.5
    eff_dis = 0.94  # battery discharging efficiency
    eff_ch = 0.94  # battery charging efficiency
    
    #emissions calculation from emission factor
    

    """
    Step 1: Create a model
    """

    model = gp.Model('Optimising scambot 2000')

    """
    Step 2: Define variables
    """
    P_grid = model.addVars(data.index, lb=-P_grid_max, ub=P_grid_max)
    SoC = model.addVars(data.index, lb=SoC_min * C_bat, ub=SoC_max * C_bat)
    P_bat_in = model.addVars(data.index, ub=P_bat_max)
    P_bat_out = model.addVars(data.index, ub=P_bat_max)
    

    """
    Step 3: Add constraints
    """
    # Power boundaries
    # Power balance formula
    model.addConstrs(P_grid[t] == data.demand[t] - data.pv_gen[t] -
                     P_bat_out[t] + P_bat_in[t] for t in range(T))

    # Battery SoC dynamics constraint
    model.addConstrs(SoC[t] == SoC[t - 1] + (P_bat_in[t] * Delta_t * eff_ch)
                     - (P_bat_out[t] * Delta_t) / eff_dis for t in range(1, T))

    model.addConstr(SoC[0] == SoC0 * C_bat + (P_bat_in[0] * Delta_t * eff_ch)
                    - (P_bat_out[0] * Delta_t) / eff_dis)

    model.addConstr(P_bat_in[0] == (
        SoC[0] - SoC0 * C_bat) / (Delta_t * eff_ch))
    model.addConstr(P_bat_out[0] == (
        (SoC0 * C_bat - SoC[0]) * eff_dis) / Delta_t)
    
    #emission cap
    if max_emission != None:
        model.addConstr(gp.quicksum(data.emission_factor[t] * P_grid[t] * Delta_t for t in range(T)) <= max_emission)
    

    """
    Step 4: Set objective function
    """
    obj_cost = gp.quicksum(data.price[t] * P_grid[t] * Delta_t for t in range(T))
    
    obj_emission = gp.quicksum(data.emission_factor[t] * P_grid[t] * Delta_t for t in range(T))

    """
    Step 5: Solve model
    """
    if optimisation_target == "cost":
        model.setObjective(obj_cost, gp.GRB.MINIMIZE)
    else:
        model.setObjective(obj_emission, gp.GRB.MINIMIZE)

    
    
    
    model.optimize()
    assert model.status == gp.GRB.OPTIMAL, 'The model could not be resolved'

    """
    Step 6: Print variables values for optimal solution
    """
    data['grid'] = model.getAttr('x', P_grid).values()
    data['battery_charge'] = model.getAttr('x', SoC).values()
    data['battery_in'] = model.getAttr('x', P_bat_in).values()
    data['battery_out'] = model.getAttr('x', P_bat_out).values()
    data['battery_power'] = data['battery_in'] - data['battery_out']
    del data['battery_in']
    del data['battery_out']

    return data

    
