# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:13:42 2020

@author: Mushtahid
"""
# Import modules
import random # To generate a random number to decide how to move agents
import operator # To get the larger x value of the agents
import matplotlib.pyplot # To plot a scatter graph of the agents

# Create agent list
agents = []

# Append the agent list to add agent0.
# y0 and x0 replaced by random integers to make it more efficient and cleaner
agents.append([random.randint(0,99), random.randint(0,99)])
print(agents)

# Check the initial coordinates of agent0
print("Initial position of agent0:", "y0:", agents[0][0], ", " "x0:", agents[0][1]) 

''' Randomly move agent0 by 1 step based on the random value being less 
or greater than 0.5'''
if random.random() < 0.5:
    agents[0][0] += 1
else:
    agents[0][0] -= 1

if random.random() < 0.5:
    agents[0][1] += 1
else:
    agents[0][1] -= 1
print("New position of agent0:", "y0:", agents[0][0], ", " "x0:", agents[0][1])
    
# Move agent0 again by 1 step
if random.random() < 0.5:
    agents[0][0] += 1
else:
    agents[0][0] -= 1

if random.random() < 0.5:
    agents[0][1] += 1
else:
    agents[0][1] -= 1
print("2nd New position of agent0:", "y0:", agents[0][0], ", " "x0:", agents[0][1])
    
# Add agent1 randomly within a 100X100 grid
agents.append([random.randint(0,99), random.randint(0,99)])
print("2nd position of agent0 and starting position of agent1:", agents)
# Check the initial coordinates of agent1
print("Initial position of agent1:", "y1:", agents[1][0], ", " "x1:", agents[1][1]) 

'''Randomly move agent1 by 1 step based on the random value 
being less or greater than 0.5'''
if random.random() < 0.5:
    agents[1][0] += 1
else:
    agents[1][0] -= 1

if random.random() < 0.5:
    agents[1][1] += 1
else:
    agents[1][1] -= 1 
print("New position of agent1:", "y1:", agents[1][0], ", " "x1:", agents[1][1])
    
# Move agent1 again by 1 step
if random.random() < 0.5:
    agents[1][0] += 1
else:
    agents[1][0] -= 1

if random.random() < 0.5:
    agents[1][1] += 1
else:
    agents[1][1] -= 1
# Check the 2nd new position of agent0 after moving 2 steps
print("2nd New position of agent1:", "y1:", agents[1][0], ", " "x1:", agents[1][1])

# Calculate and Print the distance between the agent 0 & 1
distance = (((agents[0][0]-agents[1][0])**2) + ((agents[0][1]-agents[1][1])**2))**0.5
print("Distance between agents 0 & 1:", distance)

#The agent at the furthest east(largest x)
print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))

#Plot agents in a scatter graph
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
matplotlib.pyplot.scatter(agents[0][1],agents[0][0])
matplotlib.pyplot.scatter(agents[1][1],agents[1][0])
#Color the furthest east agent red
matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')
matplotlib.pyplot.show()


