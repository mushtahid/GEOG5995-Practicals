# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 10:40:23 2020

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

r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
print(td_ys)
print(td_xs)

environment =[]
agents = []
num_of_agents = 10 
' No. of steps for agents. changed to a local variable inside gen_function'
num_of_iterations = 100
neighbourhood = 20 # Agents search for close neighbours to share resources

#??
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

#ax.set_autoscale_on(False) 

# Make agents
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)    
    agents.append(agentframework.Agent(environment, agents, x, y))
    
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
    # for j in range(num_of_iterations):
    ' I moved num_of_iterations to gen_function!'
    #random.shuffle(agents) 
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
               
    #if random.random() < 0.1: 
    'so this has to change to some store value?'
    'do we need a for loop?'
    for i in range(num_of_agents):
        if agents[i].store > 500: #trying to make each agent eat some!
            carry_on = False 
            print("stopping condition")  
        
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

def gen_function(): # what is this b?
    'This is the no. of iteration?'
    num_of_iterations = 0 #This is the iteration no.?
    global carry_on # Not actually needed as we're not assigning, but clearer
    while (num_of_iterations < 100) & (carry_on):
        yield num_of_iterations # Returns control and waits next call
        num_of_iterations = num_of_iterations + 1


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
