# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:13:42 2020

@author: Mushtahid
"""
# Import modules
import random
#import operator # To get the larger x value of the agents
import matplotlib.pyplot # To plot a scatter graph of the agents
# import time # To calculate the time taken to process sections of codes
import agentframework # Contains agent class
import csv # To read csv files

environment =[] # Environment list
agents = [] # Agents list
num_of_agents = 10 # No. of agents
num_of_iterations = 100 # No. of steps for agents
neighbourhood = 20 # Agents search for close neighbours to share resources

# Make agents
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, agents))
#print("Initial coordinates (y,x) of agents:", agents)


# Get this into your agent, and print another agent's y or x to prove it
# Trying to prove agent list inside agent but failed.  
# for a in range(len(agents)): 
#     print(a)  

# Create environment
f = open('in.txt', newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:
    rowlist = []
    for value in row:
        rowlist.append(value)
    environment.append(rowlist)
f.close()

# Move agents 
for j in range(num_of_iterations):
    random.shuffle(agents)
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)

   
# # Time to process ditance calculation
# start = time.process_time() # Start timing

# # End timing calculation
# end = time.process_time() 
# print("Time to calculate the distances: " + str(end - start)) 

#The agent at the furthest east(largest x)
#print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))

# Plot agents in a scatter graph with environment
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
matplotlib.pyplot.imshow(environment)
## For-loop to plot all agents
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
##Color the furthest east agent red
#matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')
matplotlib.pyplot.show()
