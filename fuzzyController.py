
# Pedro Paulo de Freitas Junior 35291
# ppedrofreitas@outlonormal.com.br

"""
Develop a fuzzy controller for a heating system
to keep the water temperature (TA) constant at 30 degrees.
Data:
input -> external temperature (tempExterna)
output -> heater intensity (intAquecedor)
cte -> water temperature (TA)
"""

import skfuzzy as fuzzy
import skfuzzy.control as ctrl
import numpy as num
import math
#import matplotlib.pyplot as img

# Antecedent (input/sensor) variable for a fuzzy control system.
tempExterna = ctrl.Antecedent(num.arange(-10, 30, 1), 'tempExterna')
# Consequent (output/control) variable for a fuzzy control system.
intAquecedor = ctrl.Consequent(num.arange(0, 100, 1), 'intAquecedor') 

"""
pertinencia- tempExterna
trimf - Triangular membership function generator.
"""
tempExterna['cold'] = fuzzy.trimf(tempExterna.universe, [-10, -10, 0])
tempExterna['kinda_cold'] = fuzzy.trimf(tempExterna.universe, [-8, 0, 8])
tempExterna['cool'] = fuzzy.trimf(tempExterna.universe, [0, 10, 20])
tempExterna['kinda_normal'] = fuzzy.trimf(tempExterna.universe, [10, 20, 30])
tempExterna['normal'] = fuzzy.trimf(tempExterna.universe, [20, 30, 30])
# tempExterna.view()
# img.savefig('pertinencia_tempExterna.png')

"""
#pertinencina - intAquecedor
trapmf - Trapezoidal membership function generator.
"""
intAquecedor['low'] = fuzzy.trapmf(intAquecedor.universe, [0, 5, 10, 15])
intAquecedor['kinda_low'] = fuzzy.trapmf(intAquecedor.universe, [0, 5, 6, 20])
intAquecedor['medium'] = fuzzy.trapmf(intAquecedor.universe, [15, 30, 45, 67])
intAquecedor['kinda_high'] = fuzzy.trapmf(intAquecedor.universe, [60, 70, 80, 90])
intAquecedor['high'] = fuzzy.trapmf(intAquecedor.universe, [90, 95, 100, 100])
# intAquecedor.view()
# img.savefig('pertinencia_intAquecedor.png')

""" 
rules
if tempExterna is cold then intAquecedor is high			
if tempExterna is kinda_cold then intAquecedor is kinda_high			
if tempExterna is cool then intAquecedor is medium			
if tempExterna is kinda_normal then intAquecedor is kinda_low			
if tempExterna is normal then intAquecedor is low			
"""
# Rule in a fuzzy control system, connecting antecedent(s) to consequent(s).
rule1 = ctrl.Rule(tempExterna['cold'], intAquecedor['high'])
rule2 = ctrl.Rule(tempExterna['kinda_cold'], intAquecedor['kinda_high'])
rule3 = ctrl.Rule(tempExterna['cool'], intAquecedor['medium'])
rule4 = ctrl.Rule(tempExterna['kinda_normal'], intAquecedor['kinda_low'])
rule5 = ctrl.Rule(tempExterna['normal'], intAquecedor['low'])

# Base class to contain a Fuzzy Control System.
control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
# Calculate results from a ControlSystem.
sistema = ctrl.ControlSystemSimulation(control)

print('\tTE[°C]   \tIA[%]   \t  TA[°C]')

for i in range(-5, 26):
  
    te = sistema.input['tempExterna'] = i 
    
    # Compute the fuzzy system.
    sistema.compute()

    ia = sistema.output['intAquecedor']

    # Simulation formula
    ta = te + ia/2.7 + 5*abs(math.sin(35291/500))
    
    print('\t%d' %te, '\t\t\t%d' %ia, '\t\t\t', round(ta, 5))

