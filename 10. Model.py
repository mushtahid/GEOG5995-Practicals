# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 07:32:46 2020

@author: Mushtahid
"""

# Import modules
import tkinter
import random
import operator

import matplotlib 
matplotlib.use('TkAgg')

import matplotlib.pyplot
import matplotlib.animation
#import time
import agentframework
import csv

import requests
import bs4

# Scrape web data to initialise model
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
# print(td_ys)
# print(td_xs)

#a = agentframework.Agent() (https://bit.ly/3noK3Dn) Where is it? It's
# not necessary. Was just there for testing.


num_of_agents = 10 
num_of_iterations = 100
neighbourhood = 20 # Agents search for close neighbours to share resources
environment =[]
agents = []


#??
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

#ax.set_autoscale_on(False) 

# Make the agents.
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)    
    agents.append(agentframework.Agent(environment, agents, x, y))
    # If I remove x and y why does it still seem to be working?
    # Removing environment and agent the code breaks down

    
# Create environment

# f = open('in.txt', newline='')
# reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
# for row in reader:
#     rowlist = []
#     for value in row:
#         rowlist.append(value)
#     environment.append(rowlist)
# f.close()

# Change the reader to while loop as it eliminates f.close()
with open('in.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)




# Set Carry on true (for store value)
carry_on = True

# Set animation
def update(frame_number):
    
    fig.clear()
    global carry_on # Why is this necessary here?
    
    # Move agents 
    #for j in range(num_of_iterations):
    ## If I keep the num_of_iterations then it doesn't work!
    ## random.shuffle(agents) # Need to get this back!
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
               
    #if random.random() < 0.1: 
    for i in range(num_of_agents):
        if agents[i].store > 500: #trying to make each agent eat some!
            carry_on = False 
            print("Stopping condition") #Why does it print multiple times?
        
    # Plot agents in a scatter graph with environment
    ## For-loop to plot all agents
    for i in range(num_of_agents):
        matplotlib.pyplot.ylim(0, 99)
        matplotlib.pyplot.xlim(0, 99)
        matplotlib.pyplot.imshow(environment)
        " I am calling x and y first. but in animatedmodel2.py it's y and x"
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
        #print(agents[i].x, agents[i].y)
        ##Color the furthest east agent red
        #matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')

def gen_function(): 
    'This is the no. of iteration?'
    a = 0
    global carry_on # Not actually needed as we're not assigning, but clearer
    while (a < 100) & (carry_on):
        yield a # Returns control and waits next call
        a = a + 1

def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

# Build GUI
root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

tkinter.mainloop() # Wait for interactions.



# import tkinter
# def run():
#     pass

# # Just showing menu elements
# root = tkinter.Tk()
# menu_bar = tkinter.Menu(root)
# root.config(menu=menu_bar)
# model_menu = tkinter.Menu(menu_bar)
# menu_bar.add_cascade(label="Model", menu=model_menu)
# model_menu.add_command(label="Run model", command=run)

# tkinter.mainloop() # Wait for interactions.

   
# # Time to process ditance calculation
# start = time.process_time() # Start timing

# # End timing calculation
# end = time.process_time() 
# print("Time to calculate the distances: " + str(end - start)) 

#The agent at the furthest east(largest x)
#print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))
