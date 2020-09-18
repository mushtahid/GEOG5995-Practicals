# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:13:42 2020

@author: Mushtahid
"""

import random

# Set up agent 0, random starting point within a 100X100 grid.
y0 = random.randint(0,99)
x0 = random.randint(0,99)




# Random walk one space.
if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1
    
if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1



# Random walk one space.
if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1
    
if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1







# Set up agent 1, random starting point within a 100X100 grid.
y1 = random.randint(0,99)
x1 = random.randint(0,99)



# Random walk one space.
if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1
    
if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1

print(y1, x1)

# Random walk one space.
if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1
    
if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1

print(y1, x1)



#Distance between two agents
import math

answer = math.sqrt(((y0-y1) ** 2) + ((x0-x1) ** 2))

print (answer)

