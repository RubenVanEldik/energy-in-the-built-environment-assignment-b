# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:06:06 2017

@author: alska001
Example1: First model

Step 0: Import functions from the gurobipy module
"""
import gurobipy as gp
"""
Step 1: Create a model
"""
m=gp.Model()
"""
Step 2: Define variables
"""
x1=m.addVar(vtype=gp.GRB.BINARY, name="x1")
x2=m.addVar(vtype=gp.GRB.BINARY, name="x2")
x3=m.addVar(vtype=gp.GRB.BINARY, name="x3")

"""
Step 3: Add constraints
"""
con1=m.addConstr(x1 + 2*x2 + 3*x3 <= 4)
con2=m.addConstr(x1 + x2 >= 1)

"""
Step 4: Set objective function
"""
m.setObjective(x1 + x2 + 2*x3, gp.GRB.MAXIMIZE)

"""
Step 5: Solve model
"""
m.optimize()
"""
Step 6: Print variable values for optimal solution
"""
for v in m.getVars():
    print(v.varName, v.x)

#print("x1", 1)