# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:13:42 2020

@author: Mushtahid
"""
# Import modules
import operator # To get the larger x value of the agents
import matplotlib.pyplot # To plot a scatter graph of the agents
import time # To calculate the time taken to process sections of codes
import agentframework # Contains agent class
import csv # To read csv files

# Set random seed to help with checking calculations and getting
# same results

# Function to calculate distance between agents
def distance_between(a, b):
    """
    Calculate and returns the distance between agents a and b.
    ----------
    a : TYPE
        DESCRIPTION.
    b : TYPE
        DESCRIPTION.

    Returns
    -------
    Distance between agents a and b.
    """
    return (((a.x-b.x)**2) + ((a.y-b.y)**2))**0.5


environment =[] # Environment list
agents = [] # Agents list
num_of_agents = 10 # No. of agents
num_of_iterations = 100 # No. of steps for agents

# Make agents
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment))
#print("Initial coordinates (y,x) of agents:", agents)

# Create environment
f = open('in.txt', newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:
    rowlist = []
    for value in row:
        rowlist.append(value)
    environment.append(rowlist)
    print(reader)
f.close()

# Move agents 
for j in range(num_of_iterations):
    for i in range(num_of_agents):
        agents[i].move()
   
# Time to process ditance calculation
start = time.process_time() # Start timing

# Distance calculation
distance = distance_between(agents[0], agents[1])
maxd = distance # Maximum distance between the agents
mind = distance # Minimum distance between the agents    
print("a b distance")
for a in range(len(agents)): 
    for b in range(a+1, len(agents)): # a+1 to prevent repeting the same agent
        distance = distance_between(agents[a], agents[b])
        print(a, b, distance)  
        maxd=max(maxd, distance)
        mind=min(mind, distance)
print("Maximum distance:", maxd)
print("Minimum distance:", mind)

# End timing calculation
end = time.process_time() 
print("Time to calculate the distances: " + str(end - start)) 

#The agent at the furthest east(largest x)
#print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))

# Plot agents in a scatter graph with environment
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
## For-loop to plot all agents
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
##Color the furthest east agent red
#matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()
