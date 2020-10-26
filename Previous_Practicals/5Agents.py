# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:13:42 2020

@author: Mushtahid
"""
# Import modules
import operator # To get the larger x value of the agents
import matplotlib.pyplot # To plot a scatter graph of the agents
import time # To calculate the time taken to sections of codes
import agentframework

# Set random seed to help with checking calculations and getting
# same results

a = agentframework.Agent()
print(a.y, a.x)
a.move()
print(a.y, a.x)

# Create function to calculate distance between two agents in agent list
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


# Set the number of agents
num_of_agents = 10
# Set number of iterations (no. of steps) for agents
num_of_iterations = 100
# Create agent list
agents = []



# Make agents using for-loop.
# y and x replaced by random integers to make it more efficient and cleaner
for i in range(num_of_agents):
    agents.append(agentframework.Agent())
#print("Initial coordinates (y,x) of agents:", agents)

'''Nested for-loops to move the agents. num_of_agents is within 
num_of_iterations because all agents will move 1 step at a time and then the 
next until the total number of steps are completed).
Torus is used to adjust and prevent agents going off edge''' 
# 1st for-loop for total number of steps
for j in range(num_of_iterations):
    ## 2nd for-loop to move all agents 1 step on random value being < or >=0.5 
    for i in range(num_of_agents):
        agents[i].move()
   

# Print new coordinates of all agents 
#print("New coordinates (y,x) of agents:", agents)

# Timing the distance calculation
start = time.process_time() # Start timing

# Distance calculation
distance = distance_between(agents[0], agents[1])
maxd = distance # Maximum distance between the agents
mind = distance # Minimum distance between the agents    
# Calculate distance between agents
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
# Print the time to calculate the distances
print("Time to calculate the distances: " + str(end - start)) 

#The agent at the furthest east(largest x)
#print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))

# Plot agents in a scatter graph
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
## For-loop to plot all agents
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
##Color the furthest east agent red
#matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')
matplotlib.pyplot.show()

