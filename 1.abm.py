# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:13:42 2020

@author: Mushtahid
"""
# Import modules
import random

# Set random seed to get consistent results everytme the script is run


# Make y and x coordinate variables of agent0
y0 = 50
x0 = 50

# To check the initial coordinates of agent0
print("Initial position of agent0:", "y0:", y0, ", " "x0:", x0) 



''' Randomly move agent0 by 1 step based on the random value being less 
or greater than 0.5'''
if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1

if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1
    
# To check the new position of agent0 after being altered based on random value
print("New position of agent0:", "y0:", y0, ", " "x0:", x0)
    
# Move agent0 again by 1 step
if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1

if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1

# To check the 2nd new position of agent0
print("2nd New position of agent0:", "y0:", y0, ", " "x0:", x0)
    
# Make y and x coordinate variables of agent1
y1 = 50
x1 = 50

# To check the initial coordinates of agent0
print("Initial position of agent1:", "y1:", y1, ", " "x1:", x1) 



'''Randomly move agent1 by 1 step based on the random value 
being less or greater than 0.5'''
if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1

if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1
    
# To check the new position of agent1 after being altered based on random value
print("New position of agent1:", "y1:", y1, ", " "x1:", x1)
    
# Move agent1 again by 1 step
if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1

if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1

# To check the 2nd new position of agent0
print("2nd New position of agent1:", "y1:", y1, ", " "x1:", x1)

# Calculate the distance between the two agents
distance = (((y0-y1)**2) + ((x0-x1)**2))**0.5

# Print the distance between agents 0 & 1
print("Distance between agents 0 & 1:", distance)

