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

#a = agentframework.Agent() (https://bit.ly/3noK3Dn)

# Set up lists in the begining
n_ag = input('Enter number of sheep: ')
try:
    num_of_agents = int(n_ag)
except:
    num_of_agents = 10
    print('Invalid characters/No number entered! Model will run with default of 10 sheep')
n_it = input('Enter number of iterations: ')
try:
    num_of_iterations = int(n_it)
except:
    num_of_iterations = 100
    print('Invalid characters/No number entered! Model will run with default of 100 iterations') 
neighbourhood = 40# Agents search for close neighbours to share resources.
min_str = 900 # Each agent must have a min store val of 900 to reach stopping cond.
totalscorelist = [] # For use in writing the total store in a csv file
totalstore = 0 # For storing the toal amount as float
environment =[] # Create environment list first before agent list.
agents = []
carry_on = True # Carry on True for store value

#??
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
# ax.set_autoscale_on(False) 
 
# Create Environment (before moving the agents https://bit.ly/3jPX3Qq)
with open('in.txt', newline='') as f:
    env_reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in env_reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)
        
# Write environment in a file.
with open('environmentout.txt', 'w', newline='') as f2:     
   env_writer = csv.writer(f2)     
   for row in environment:         
        env_writer.writerow(row)
        
# Make the agents.
for i in range(num_of_agents):
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)    
    agents.append(agentframework.Agent(environment, agents, y, x))
    # If I remove x and y why does it still seem to be working?
    # But removing environment and agent, the code breaks down

# Set animation
def update(frame_number):
    
    fig.clear()
    global carry_on
    str_list = [] # List of Store value of agents. Used to meet carry_on conditions
    # Shuffle agents list before each iteration (https://bit.ly/3k1ydgg)
    random.shuffle(agents)
    # Move agents
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        # agents[i].sickup() # Uncomment to make agents vomit out 50 if eats > 100
        # print(i, agents[i].store)
        str_list.append(agents[i].store) # Adds store value to str_list
        # print(str_list)     
    print(str_list)
    # print(min(str_list))
    # Make sure each agent eats a minimum > min_str (https://bit.ly/2SI7pWD)  
    if min(str_list) > min_str:
        carry_on = False
        print(f"Stopping condition. Each agent has min store value of {min_str}.")      
              
    # Plot agents in a scatter graph with environment
    for i in range(num_of_agents):
        matplotlib.pyplot.ylim(0, len(environment))
        matplotlib.pyplot.xlim(0, len(environment[0]))
        # matplotlib.pyplot.ylim(0, 99)
        # matplotlib.pyplot.xlim(0, 99)
        matplotlib.pyplot.imshow(environment)
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y)
        #print(agents[i].x, agents[i].y)
        ##Color the furthest east agent red
        #matplotlib.pyplot.scatter(max(agents, key=operator.itemgetter(1))[1], max(agents, key=operator.itemgetter(1))[0], color='red')

# Utilise num_of_iterations and carry on conditions
def gen_function(): 
    a = 0 # To match with num_of_iterations
    global carry_on # Not actually needed as we're not assigning, but clearer.
    while (a < num_of_iterations) & (carry_on):
        yield a # Returns control and waits next call
        a = a + 1
        print(f"Iteration no {a}") # Uncomment to show iteration number
    

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

# Find total amount stored by all agents (https://bit.ly/30VLAXX)
## Calculate the total store value
for i in range(num_of_agents):
        totalstore += agents[i].store
        # print(totalstore)
totalscorelist.append(totalstore)
# print(totalscorelist)
## Write the total stored amount in another file
with open('total_store_amount.txt', 'a', newline='') as f3:     
    store_writer = csv.writer(f3, delimiter=' ')     
    store_writer.writerow(totalscorelist)

# Print each agent's location and store value
for i in range(num_of_agents):
    print(i, agents[i])
    

  
# # Time to process ditance calculation
# start = time.process_time() # Start timing

# # End timing calculation
# end = time.process_time() 
# print("Time to calculate the distances: " + str(end - start)) 

#The agent at the furthest east(largest x)
#print("Furthest east agent:", max(agents, key=operator.itemgetter(1)))
