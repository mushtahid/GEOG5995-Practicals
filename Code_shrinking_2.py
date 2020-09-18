# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:13:42 2020

@author: Mushtahid
"""
# Import modules
import random # To generate a random number to decide how to move agents
import operator # To get the larger x value of the agents
import matplotlib.pyplot # To plot a scatter graph of the agents


# Set the number of agents
num_of_agents = 10
# Set number of iterations (no. of coordination changes) for agents
num_of_iterations = 100


# Create agent list
agents = []


# Append the agent list to add agents using for-loop.
# y0 and x0 replaced by random integers to make it more efficient and cleaner
for i in range(num_of_agents):
    agents.append([random.randint(0,99), random.randint(0,99)])
print("Initial coordinates (y,x) of agents:", agents)

'''Nested for-loops. num_of_agents is within num_of_iterations because all 
agents will move 1 step at a time and then the next (with a total step set by
num_of_iterations)''' 
# 1st for-loop for total number of steps
for j in range(num_of_iterations):
    ## 2nd For-loop to move all agents 1 step on random value being < or >=0.5 
    for i in range(num_of_agents):
        ### Move Y coordinate
        if random.random() < 0.5:
            agents[i][0] += 1
        else:
            agents[i][0] -= 1
        ### Move X coordinate
        if random.random() < 0.5:
           agents[i][1] += 1
        else:
           agents[i][1] -= 1
        ### Check if off edge and adjust.
        if agents[i][0] < 0:
            agents[i][0] = 99
        if agents[i][1] < 0:
            agents[i][1] = 99
        if agents[i][0] > 99:
            agents[i][0] = 0
        if agents[i][1] > 99:
            agents[i][1] = 0
# Print new coordinates of all agents 
print("New coordinates (y,x) of agents:", agents)
    
    
# Calculate the distance between the agent 0 & 1
# distance = (((agents[0][0]-agents[1][0])**2) + ((agents[0][1]-agents[1][1])**2))**0.5
# print("Distance between agents 0 & 1:", distance)


#The agent at the furthest east(largest x)
print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))

# Plot agents in a scatter graph
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
## For-loop to plot all agents
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i][1],agents[i][0])
##Color the furthest east agent red
matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')
matplotlib.pyplot.show()


