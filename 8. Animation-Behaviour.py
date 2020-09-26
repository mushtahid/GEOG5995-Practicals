# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 09:24:36 2020

@author: Mushtahid
"""

# Import modules
import random
import matplotlib.pyplot
import matplotlib.animation
#import time
import agentframework
import csv

environment =[]
agents = []
num_of_agents = 10 # No. of agents
num_of_iterations = 100 # No. of steps for agents
neighbourhood = 20 # Agents search for close neighbours to share resources

#
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

#ax.set_autoscale_on(False)

# Make agents
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, agents))

# Create environment
f = open('in.txt', newline='')
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:
    rowlist = []
    for value in row:
        rowlist.append(value)
    environment.append(rowlist)
f.close()

#
def update(frame_number):
    fig.clear()   
    # Move agents 
    #for j in range(num_of_iterations):
        #random.shuffle(agents)
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        
    # Plot agents in a scatter graph with environment
    ## For-loop to plot all agents
    for i in range(num_of_agents):
        matplotlib.pyplot.ylim(0, 99)
        matplotlib.pyplot.xlim(0, 99)
        matplotlib.pyplot.imshow(environment)
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
        print(agents[i].x, agents[i].y)
        ##Color the furthest east agent red
        #matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')
animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=num_of_iterations)
matplotlib.pyplot.show()

   
# # Time to process ditance calculation
# start = time.process_time() # Start timing

# # End timing calculation
# end = time.process_time() 
# print("Time to calculate the distances: " + str(end - start)) 

#The agent at the furthest east(largest x)
#print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))


