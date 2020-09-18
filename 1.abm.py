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


# Randomly move ageon 0 by 1 based on the random value being less or greater than 0.5
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


