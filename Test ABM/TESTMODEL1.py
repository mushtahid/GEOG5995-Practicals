# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 09:26:33 2020

@author: User
"""
import TESTAF1 as aaf
import tkinter
import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation
import random
import csv

environment = []
animals = []
sheep = []
wolves = []
no_sheep = 10
no_wolves = 5
no_iterations = 5
proximity = 50
no_animals = no_sheep + no_wolves

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

with open('in.txt', newline='') as f:
    env_reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in env_reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)

for i in range(no_sheep):
    sheep.append(aaf.Sheep(animals, wolves, sheep, environment)) 
print('No sheep', len(sheep))

for i in range(no_wolves):
    wolves.append(aaf.Wolf(animals, wolves, sheep, environment)) 
print('No wolves', len(wolves))

'The problem with animals is that it is spawning different set of animals'
# for i in range(len(animals)):
#     for j in range(i+1, len(animals)):
#         distance = aaf.Animal.dist_animals(animals[i], animals[j])
#         print(i, j, distance)

def update(frame_number):
    
    fig.clear()
    # random.shuffle(wolves)
    # random.shuffle(sheep) 
    # for i in range(no_wolves):
    #     for j in range(no_sheep):
    #         distance = aaf.Animal.dist_animals(wolves[i], sheep[j])
    #         print(f"wolf{i}: {wolves[i].y},{wolves[i].x}, sheep{j}: {sheep[j].y},{sheep[j].x}, d={distance}")
       
    for i in range(len(wolves)):
        wolves[i].move()
        print(i, 'Wolves', wolves[i])
        
    for i in range(len(sheep)):
        sheep[i].move()
        sheep[i].eat()
        print(i, 'Sheep', sheep[i])
        
    # for i in range(len(wolves)):
    #     for j in range(len(sheep)):
    #         distance = aaf.Animal.dist_animals(wolves[i], sheep[j])
    #         print(f"wolf{i}: {wolves[i].y},{wolves[i].x}, sheep{j}: {sheep[j].y},{sheep[j].x}, d={distance}")
    #         if distance < proximity:
    #             wolves[i].store += sheep[j].store
    #             sheep[j].store = 0
    #             sheep.remove(sheep[j])
    #             continue
            
    for i in range(len(wolves)):
        sheep_count = -1
        for j in sheep[:]:
            sheep_count += 1
            distance = aaf.Animal.dist_animals(wolves[i], j)
            # print(f"wolf{i}: {wolves[i].y},{wolves[i].x}, sheep{j}: {sheep[j].y},{sheep[j].x}, d={distance}")
            print(f"wolf {i}: {wolves[i].y},{wolves[i].x}, sheep: {sheep_count} {j.y},{j.x}, d={distance}")
            if distance < proximity:
                wolves[i].store += j.store
                j.store = 0
                print('Sheep eaten', sheep_count, j, 'by Wolf', i)
                sheep.remove(j)
                break
    
    plt.ylim(0, len(environment))
    plt.xlim(0, len(environment[0])) 
    plt.imshow(environment)
    for i in range(len(sheep)):
        plt.scatter(sheep[i].x, sheep[i].y, marker="p")
    for i in range(len(wolves)):
        plt.scatter(wolves[i].x, wolves[i].y, marker="v")

def gen_function(): 
    a = 0 
    # print(f"***Iteration no {a} ***")
    while (a < no_iterations):
        print(f"***Iteration no {a}***")
        yield a
        # print(f"***Iteration no {a} \u2191 ***")
        a = a + 1
        # print(f"***Iteration no {a} \u2191 ***")

def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()
   

root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)

tkinter.mainloop()

# print((((146 - 214)**2) + ((139 - 244)**2))**0.5)


