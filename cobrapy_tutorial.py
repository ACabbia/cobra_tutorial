#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 15:23:17 2017
@author: acabbia
"""

# COBRApy tutorial:
 
#### 1) Getting Started:
#### 1.1) Load and inspect a model

import cobra.test
from os.path import join

# in this example we will load a small test model: 
data_dir = cobra.test.data_dir

model = cobra.io.read_sbml_model(join(data_dir, "mini_fbc2.xml")) # <- try to change the argument to the path of the folder where you saved the model

# The model has several "attributes" that are accessed through the dot notation:
model. # <-- press <TAB> key to inspect model attributes

# Reactions, Metabolites and Genes are attributes that list cobra.Reaction, cobra.Metabolite and cobra.Gene objects respectively:

print(len(model.reactions))
print(len(model.metabolites))
print(len(model.genes))

# we can inspect the content of these list with a for loop: 
for m in model.metabolites: print(m)

# metabolite notation: 
# eg atp_c = abbreviation + cellular compartment
model.compartments

# Reaction and Metabolites objects can be retrieved by their 'ID' using the .get_by_id() function:

# 1.2 ) Metabolites
nadh = model.metabolites.get_by_id('nadh_c')

# we can access information like full name and compartment
nadh.name
nadh.compartment
# or we can see NADH charge or formula:
nadh.charge
nadh.formula
# or see which in which reactions nadh is used:
nadh.reactions 

# 1.3) Reactions
# Working with reaction is similar: we can access them through 'ID'
PYK = model.reactions.get_by_id('PYK')
# full name and reactions catalyzed
PYK.name
PYK.reaction
# we can view ( and set ) reaction bounds: 
PYK.bounds
PYK.bounds = -500 , 500
# and check reaction reversibility
PYK.reversibility


## 2) Building and expanding a model:
#This example demonstrates how to create reaction, and then add it to a test model:

from cobra import Model, Metabolite , Reaction

# create an empty test model:
test_model = Model("Test model")

# create a Reaction object (Pyruvate Dehidrogenase) and define its attributes

PDH = Reaction(id = "PDH", 
               name = "Pyruvate dehidrogenase", 
               subsystem = "central carbon metabolism",
               lower_bound = 0, 
               upper_bound = 1000)

# We need to create metabolites objects as well. 
# If we were using an existing model, we could use model.metabolites.get_by_id() to get the appropriate Metabolite objects instead.

accoa = Metabolite(id = 'accoa_c',
                   name = 'Acetyl-CoA',
                   compartment = 'c')

co2 = Metabolite(id = 'co2_c',
                   name = 'CO2',
                   compartment = 'c')

coa = Metabolite(id = 'coa_c',
                   name = 'Co-enzyme A',
                   compartment = 'c')

nad = Metabolite(id = 'nad_c',
                   name = 'Nicotinamide adenine dinucleotide',
                   compartment = 'c')

nadh = Metabolite(id = 'nadh_c',
                   name = 'Nicotinamide adenine dinucleotide - reduced',
                   compartment = 'c')

pyr = Metabolite(id = 'pyr_c',
                   name = 'pyruvate',
                   compartment = 'c')

## Add the metabolites and their coefficients to the Reaction object: 

PDH.add_metabolites({   #<--- dict 
        coa   : -1,
        nad   : -1,
        pyr   : -1,
        accoa :  1,
        co2   :  1,
        nadh  :  1,
        })

### At this point the model is still empty:
print('%i reactions initially' % len(test_model.reactions))
print('%i metabolites initially' % len(test_model.metabolites))

# We add the reaction to the model, which will also add all associated metabolites:
test_model.add_reaction(PDH)

# Now there are things in the model
print('%i reaction' % len(test_model.reactions))
print('%i metabolites' % len(test_model.metabolites))

# 3) simulating with Flux Balance Analysis:

# Load test e.coli model
import cobra.test
model = cobra.test.create_test_model("ecoli")

# set objective function 
model.objective = 'ATPS4rpp'

# set LP solver
model.solver('gurobi') # or 'glpk'

# FBA optimization can be solved using Model.optimize(). 
# This will maximize or minimize (maximizing is the default) flux through the objective reactions.

solution = model.optimize()

#The Model.optimize() function will return a Solution object. A solution object has several attributes:

#the objective value
solution.objective_value

#the flux distribution
solution.fluxes

# solver status (e.g. 'optimal' or 'unfeasible')
solution.status

#4) Inspecting FBA solution
# summary method displays information on the input and output behavior of the model, along with the optimized objective:

model.summary()  #<--- must be called AFTER model.optimize() 

# input-output behavior of individual metabolites can also be inspected 
# checking (cytosolic) NADH behavior can be useful to inspect redox balance of the cell:
model.metabolites.nadh_c.summary()

# instead checking atp behavior will give us a sense of energy production and consumption:
model.metabolites.atp_c.summary()

#5) Save and export a model:

cobra.io.write_sbml_model(model, "test_model_AC.xml")

####
####

# Exercises:

# Change reaction bounds

# Add a reaction to the test model


