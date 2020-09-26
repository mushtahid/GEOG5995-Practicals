# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 09:24:36 2020

@author: Mushtahid
"""
# Import modules
import random
import operator
import matplotlib.pyplot
import matplotlib.animation
#import time
import agentframework
import csv

environment =[]
agents = []
num_of_agents = 10 # No. of agents
#num_of_iterations = 100 # No. of steps for agents
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
carry_on = True

def update(frame_number):
    
    fig.clear()
    global carry_on
    
    # Move agents 
    #for j in range(num_of_iterations):
        #random.shuffle(agents)
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        
    #if random.random() < 0.1: # so this has to change to some store vale?
    #do we need a for loop?
    for i in range(num_of_agents):
        if agents[i].store > 1000: #trying to make each agent eat some!
            carry_on = False 
            print("stopping condition")  
        
    # Plot agents in a scatter graph with environment
    ## For-loop to plot all agents
    for i in range(num_of_agents):
        matplotlib.pyplot.ylim(0, 99)
        matplotlib.pyplot.xlim(0, 99)
        matplotlib.pyplot.imshow(environment)
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
        #print(agents[i].x, agents[i].y)
        ##Color the furthest east agent red
        #matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')
def gen_function(b = [0]): # what is this b?
    num_of_iterations = 0 # This is the iteration no.?
    global carry_on # Not actually needed as we're nott assigning, but clearer?
    while (num_of_iterations < 100) & (carry_on):
        yield num_of_iterations # Returns control and waits next call???
        num_of_iterations = num_of_iterations + 1
#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=num_of_iterations)
animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
matplotlib.pyplot.show()

   
# # Time to process ditance calculation
# start = time.process_time() # Start timing

# # End timing calculation
# end = time.process_time() 
# print("Time to calculate the distances: " + str(end - start)) 

#The agent at the furthest east(largest x)
#print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))


