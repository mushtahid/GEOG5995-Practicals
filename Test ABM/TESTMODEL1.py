# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 09:26:33 2020

@author: Mushtahid
"""
import TESTAF1 as af
import tkinter
import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation
import random
random.seed(10)
import csv

environment = []
animals = []
sheep = []
wolves = []
no_sheep = 10
no_wolves = 5
no_iterations = 200
it_no = -1 # No of iterations
proximity = 50
action_dist = 5 # action refers to breeding/eating sheep...
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
    sheep.append(af.Sheep(animals, wolves, sheep, environment)) 
print('No sheep', len(sheep))

for i in range(no_wolves):
    wolves.append(af.Wolf(animals, wolves, sheep, environment)) 
print('No wolves', len(wolves))

'The problem with animals is that it is spawning different set of animals'
# for i in range(len(animals)):
#     for j in range(i+1, len(animals)):
#         distance = af.Animal.dist_animals(animals[i], animals[j])
#         print(i, j, distance)

# def gen_function(b = no_iterations):
#     a = 0
#     print('a0', a)
#     # print('')
#     # print(f"*************** ITERATION NUMBER {a} ***************")
#     while a < b:
#         print('')
#         print('a1', a)
#         print(f"*************** ITERATION NUMBER {a} ***************")
#         yield a
#         print('a2', a)
#         # print(f"*************** ITERATION NUMBER {a} ***************")
#         a += 1
#         print('a3', a)
#     # print(f"***Iteration no {a} \u2191 ***")



def gen_function(b = no_iterations):
    a = 0
    while a < b:
        yield a
        a += 1

def update(frame_number):
    fig.clear()
    global it_no
    it_no += 1
    print('')
    print(f"*************** ITERATION NUMBER {it_no} ************")
    
    # random.shuffle(wolves)
    # random.shuffle(sheep) 
    # for i in range(no_wolves):
    #     for j in range(no_sheep):
    #         distance = af.Animal.dist_animals(wolves[i], sheep[j])
    #         print(f"wolf{i}: {wolves[i].y},{wolves[i].x}, sheep{j}: {sheep[j].y},{sheep[j].x}, d={distance}")
       
    # for i in range(len(wolves)):
    #     wolves[i].move()
    #     print(i, 'Wolves', wolves[i])
        
    # for i in range(len(sheep)):
    #     print(i, 'Sheep-before moving+eating', sheep[i])
    #     sheep[i].move()
    #     sheep[i].eat()
    #     print(i, 'Sheep-after moving+eating', sheep[i])
    #     print('S.........................................')
    # print('Sheep_________________________________________')
### NEED TO ADJUST THE PRINT TAGS LATER   
    for i in range(len(sheep)):
        print('')
        print(f"------------- {i} Sheep initialised -----------")
        min_dist = 0.5*proximity # coz sheep is a prey! wolves have higer perimeter
        closest_wolf = None
        # print(min_dist) #
        # print(closest_wolf) #
        for j in range(len(wolves)): 
            # print(f"--> {i}-Sheep looping with {j}-Wolf")                
            distance = af.Animal.dist_animals(sheep[i], wolves[j])
            # print(f"--> d={distance} for {i}-Sheep ({sheep[i]}) with {j}-Wolf ({wolves[j]})") #
            if distance < min_dist:
                print(f"---> d<md+... {i}-Sheep noticed closest Wolf {j}...")
                min_dist = distance
                closest_wolf = wolves[j]
                
                print(f"---> {i}-Sheep ({sheep[i]}) detected {j}-Wolf ({wolves[j]}) within d={min_dist}")                
        if closest_wolf != None:
            print("-> CW FOUND")
            print(f"-> Before {i}-Sheep ({sheep[i]}) tries to run away from CW: ({closest_wolf})")
            sheep[i].y = (sheep[i].y + (sheep[i].y - int((sheep[i].y + closest_wolf.y)/2))) % (len(environment))
            sheep[i].x = (sheep[i].x + (sheep[i].x - int((sheep[i].x + closest_wolf.x)/2))) % (len(environment[0]))
            print(f"-> After {i}-Sheep ({sheep[i]}) tried to run away from CW ({closest_wolf})")
            print(f".......... {i} Sheep tried to run away from CW ..........")  
        else:
            print(f"-> No CW")
            print(f"-> {i}-Sheep ({sheep[i]}) will now move normally and eat")
            sheep[i].move()
            sheep[i].eat()
            print(f"-> {i}-Sheep ({sheep[i]}) after normally moving and eating")
            print(f".......... {i}-Sheep moved normally and ate.......... ")
    print('')        
    print('________________Sheep Cycle Ends________________')
    print('________________Wolf Cycle Begins________________')
    
    # for i in range(len(wolves)):
    #     print(i, 'Wolf - before moving/eating -', wolves[i])
    #     sheep_count = -1
    #     # print(f"min_dist a = {min_dist}")
    #     closest_sheep = None
    #     min_dist = proximity
    #     eaten = False
    #     for j in sheep[:]:
    #         # print(f"min_dist b = {min_dist}")
    #         sheep_count += 1
    #         distance = af.Animal.dist_animals(wolves[i], j)
    #         # if eat_dist < distance < min_dist:
    #         if distance <= eat_dist:
    #             print('>>> Sheep going to be eaten', sheep_count, j, 'by Wolf', i, wolves[i])
    #             wolves[i].store += j.store
    #             j.store = 0
    #             print('>>> Sheep eaten', sheep_count, j, 'by Wolf', i, wolves[i])
    #             sheep.remove(j)
    #             print('Eaten_________________________________________')
    #             # break # activates else after eating.
    #             # continue # no good. targets immediately another sheep. and activates else.
    #             eaten = True # works. still targets. but does not move. so fine!
    #         elif eat_dist < distance < min_dist:
    #             min_dist = distance
    #             closest_sheep = j
    #             print('>>> min_dist =', min_dist, 'Sheep', sheep_count, j, 'by Wolf', i, wolves[i])
    #             print('M.........................................')
    #     if eaten == True:
    #         #break
    #         continue # This works! it still targets but that's fine as long is it does not move!
    #     elif closest_sheep != None:
    #         print('CS+ before', closest_sheep, 'Wolf', i, wolves[i])
    #         wolves[i].y = (int((wolves[i].y + closest_sheep.y)/2)) % (len(environment))
    #         wolves[i].x = (int((wolves[i].x + closest_sheep.x)/2)) % (len(environment[0]))
    #         print('CS+ after', closest_sheep, 'Wolf', i, wolves[i])
    #         print('Y.........................................')           
    #     else:
    #         print('Else activate before', 'by Wolf', i, wolves[i])
    #         wolves[i].move()
    #         print('Else activate after', 'by Wolf', i, wolves[i])
    #         print('E.........................................')
    # print('Wolf Cycle Ends___________________________________')

    # for i in range(len(wolves)):
    #     print('')
    #     print(f"-> -----------{i}-Wolf initialised with ({wolves[i]}) -----------")
    #     #print(i, 'Wolf - before eating/moving or breeding -', wolves[i])
    #     if wolves[i].store <= 500:
    #         print(f"--> {i}-Wolf has <=500 store ({wolves[i]})")
    #         sheep_count = -1
    #         closest_sheep = None
    #         min_dist = proximity
    #         eaten = False
    #         for j in sheep[:]:
    #             sheep_count += 1
    #             print(f"---> {i}-Wolf looping with {sheep_count}-Sheep")              
    #             distance = af.Animal.dist_animals(wolves[i], j)
    #             # print(f"distance={distance} between {i}-Wolf ({wolves[i]}) and {sheep_count}-Sheep ({j})")
    #             # if eat_dist < distance < min_dist:
    #             if distance <= action_dist:
    #                 print(f"----> d<=action_dist found")
    #                 print(f"----> {i}-Wolf ({wolves[i]}) before eating {sheep_count}-Sheep ({j})")
    #                 wolves[i].store += j.store
    #                 j.store = 0
    #                 print(f"----> {i}-Wolf ({wolves[i]}) after eating {sheep_count}-Sheep ({j})")
    #                 sheep.remove(j)
    #                 eaten = True # works. still targets. but does not move. so fine!
    #                 # break # activates else after eating.
    #                 # continue # no good. targets immediately another sheep. and activates else.
    #             elif action_dist < distance < min_dist:
    #                 print(f"----> action_dist < distance < min_dist")
    #                 min_dist = distance
    #                 closest_sheep = j
    #                 print(f"----> min_dist = {min_dist} for {i}-Wolf ({wolves[i]}) with {sheep_count}-Sheep ({j})")
    #                 print('....elif adm ends. CS+...')
    #         if eaten == True:
    #             #break
    #             print(f"---> ..........eaten==True {i}-Wolf one ate CS..........")
    #             continue # This works! it still targets but that's fine as long is it does not move!
    #         elif closest_sheep != None:
    #             print(f"---> {i}-Wolf ({wolves[i]}) before moving closer to  CS-Sheep ({closest_sheep })")
    #             wolves[i].y = (int((wolves[i].y + closest_sheep.y)/2)) % (len(environment))
    #             wolves[i].x = (int((wolves[i].x + closest_sheep.x)/2)) % (len(environment[0]))
    #             print(f"---> {i}-Wolf ({wolves[i]}) after moving closer to Sheep ({closest_sheep })")
    #             print(f"..........{i}-Wolf moved closer to CS+..........")           
    #         else: #no sheep store <500
    #             print(f"--->else1 begins: {i}-Wolf ({wolves[i]}) before normal moving")
    #             wolves[i].move()
    #             print(f"--->else1 ends: {i}-Wolf ({wolves[i]}) after normal moving")
    #             print(f"....el1......{i}-Wolf moved normally..........")
    #     elif wolves[i].store > 500:
    #         print(f"--> {i}-Wolf has >500 store ({wolves[i]})")
    #         min_breed_dist = proximity
    #         bred = False
    #         closest_wolf = None
    #         for j in range(i+1, len(wolves)):
    #             print(f"---> {i}-Wolf looping with {j}-Wolf")
    #             # Why i+1: to prevent comparison? but what about second wolf?
    #             distance =  af.Animal.dist_animals(wolves[i], wolves[j])
    #             if action_dist < distance < min_breed_dist:
    #                 print('----> CW+ (ad<d<md)')
    #                 min_breed_dist = distance
    #                 closest_wolf = wolves[j]
    #                 print(f"----> min_breed_dist={min_breed_dist} for {i}-Wolf ({wolves[i]}) with CW {j}-Wolf ({wolves[j]})")
    #                 # print('>>> min_breed_dist=', min_breed_dist, 'Wolf', j, wolves[j], 'by Wolf', i, wolves[i])
    #             elif distance <= action_dist:
    #                 print(f"----> d<=ad. breeding/fight distance entered for {i}-Wolf ({wolves[i]}) with CW {j}-Wolf ({wolves[j]}")
    #                 if random.random() < 0.5:
    #                     print(f"-----> Random <0.5")
    #                     print(f"-----> {i}-Wolf ({wolves[i]}) before mating with {j}-Wolf ({wolves[j]})")
    #                     # print('>>> Wolf', j, wolves[j], 'will be mated by Wolf', i, wolves[i])
    #                     print('------> Breed code goes here')
    #                     print(f"-----> {i}-Wolf ({wolves[i]}) after mating with {j}-Wolf ({wolves[j]})")
    #                     print('_____________{i}-Wolf Mated____________')
    #                     # break # activates else after eating.
    #                     # continue # no good. targets immediately another sheep. and activates else.
    #                     bred = True # works. still targets. but does not move. so fine!
    #                 else:
    #                     print(f"-----> Random >0.5")
    #                     print(f"----->Wolf {i} {wolves[i]} does something else with Wolf {j} {wolves[j]}")
    #                     print('----->..........Something else, maybe steal food based on probability..........')
    #                     # Need to add a boolean condition
    #         if bred == True:
    #             #break
    #             print("---> bred==True {i}-Wolf")
    #             continue #( This works! it still targets but that's fine as long is it does not move!)
    #         elif closest_wolf != None:
    #             print(f"---> {i}Wolf ({wolves[i]}) before moving closer to CW-Wolf ({closest_wolf })")
    #             # print('CW+ detected (before)', closest_wolf, 'by Wolf', i, wolves[i])
    #             wolves[i].y = (int((wolves[i].y + closest_wolf.y)/2)) % (len(environment))
    #             wolves[i].x = (int((wolves[i].x + closest_wolf.x)/2)) % (len(environment[0]))
    #             print(f"---> {i}Wolf ({wolves[i]}) after moving closer to CW-Wolf ({closest_wolf })")
    #             # print('CW+ (after)', closest_wolf, 'being approached by Wolf', i, wolves[i])
    #             print('..........{i}-Wolf moved closer CW+..........')   
    #         else: # No wolf. store >700
    #             print(f"--->else2 begins: {i}-Wolf ({wolves[i]}) before normal moving")
    #             # print('Else 2 activate by Wolf', i, wolves[i])
    #             wolves[i].move()
    #             print(f"--->else2 begins: {i}-Wolf ({wolves[i]}) after normal moving")
    #             print(f"....el2...... {i}-Wolf moved normally")
    # print('__________Wolf Cycle Ends___________')
    
    wolf_count = -1
    for i in wolves[:]:
        wolf_count += 1   
        print('')
        print(f"-> -----------{wolf_count}-Wolf initialised with ({i}) -----------")
        
        if i.store <= 500:
            print(f"--> {wolf_count}-Wolf has <=500 store ({i})")
            sheep_count = -1
            closest_sheep = None
            min_dist = proximity
            eaten = False
            for j in sheep[:]:
                sheep_count += 1
                print(f"---> {wolf_count}-Wolf looping with {sheep_count}-Sheep")              
                distance = af.Animal.dist_animals(i, j)
                # print(f"distance={distance} between {i}-Wolf ({wolves[i]}) and {sheep_count}-Sheep ({j})")
                # if eat_dist < distance < min_dist:
                if distance <= action_dist:
                    # eats the first sheep at action distance. so should not loop through the other ones.
                    print(f"----> d<=action_dist found")
                    print(f"----> {wolf_count}-Wolf ({i}) before eating {sheep_count}-Sheep ({j})")
                    i.store += j.store
                    j.store = 0
                    print(f"----> {wolf_count}-Wolf ({i}) after eating {sheep_count}-Sheep ({j})")
                    sheep.remove(j)
                    eaten = True # works. still targets. but does not move. so fine!
                    break # ?activates else after eating.
                    # continue # no good. targets immediately another sheep. and activates else.
                elif action_dist < distance < min_dist:
                    print(f"----> action_dist < distance < min_dist")
                    min_dist = distance
                    closest_sheep = j
                    print(f"----> Min Distance = {min_dist} for {wolf_count}-Wolf ({i}) with {sheep_count}-Sheep ({j})")
                    print('....elif adm ends. CS+...')
            if eaten == True:
                #break
                print(f"---> ..........Eaten={eaten}. {wolf_count}-Wolf one ate CS {sheep_count}-Sheep ({j})..........")
                continue # This works! it still targets but that's fine as long is it does not move!?
                
            elif closest_sheep != None:
                print(f"--> {wolf_count}-Wolf ({i}) before moving closer to  CS-Sheep ({closest_sheep })")
                i.y = (int((i.y + closest_sheep.y)/2)) % (len(environment))
                i.x = (int((i.x + closest_sheep.x)/2)) % (len(environment[0]))
                print(f"--> {wolf_count}-Wolf ({i}) after moving closer to Sheep ({closest_sheep })")
                print(f"..........{wolf_count}-Wolf moved closer to CS+..........")           
            else: #no sheep and store <500
                print(f"-->else1 begins: {wolf_count}-Wolf ({i}) before normal moving")
                i.move()
                print(f"-->else1 ends: {wolf_count}-Wolf ({i}) after normal moving")
                print(f"....el1......{wolf_count}-Wolf moved normally..........")
        elif i.store > 500: # Wolf tries to breed / fight
            print(f"--> {wolf_count}-Wolf has >500 store ({i})")
            min_dist = proximity
            action = False
            fight = False
            breed = False
            closest_wolf = None
            wolf2_count = -1
            for j in wolves[1:]: # so that i wolf is spared! and action not duplicated for same pair.
                wolf2_count += 1
                print(f"---> {wolf_count}-Wolf looping with {wolf2_count}-Wolf")
                distance =  af.Animal.dist_animals(i, j)
                if action_dist < distance < min_dist:
                    print('----> CW+ (ad<d<md)')
                    min_dist = distance
                    closest_wolf = j
                    print(f"----> Min distance={min_dist} for {wolf_count}-Wolf ({i}) with CW {wolf2_count}-Wolf ({j})")  
                elif distance <= action_dist:
                    print(f"----> d<=ad. breeding/fight proximity of {distance}<={action_dist} entered by {wolf_count}-Wolf ({i}) with CW {wolf2_count}-Wolf ({j}")
                    if j.store > 500:
                        print(f"----->The opposition: {wolf2_count}-Wolf ({j} has MORE than 500 store")
                        if random.random() < 0.5: #50% chance of meeting a female!
                            print(f"------> Random <0.5. So the wolves will mate.")
                            print(f"------> {wolf_count}-Wolf ({i}) before mating with {wolf2_count}-Wolf ({j})")
                            average = ((i.store + j.store)/2)
                            i.store = average - 200 # 200 is energy for mating.
                            j.store = average - 200 # They will share average energy - 200 energy for mating.
                            print(f"------> {wolf_count}-Wolf ({i}) after mating with {wolf2_count}-Wolf ({j})")
                            wolves.append(i) # Added new wolf to the list.
                            print('_____________{wolf_count}-Wolf Mated____________')
                            breed = True
                            print(f"Breed = {breed}")
                            print('_____________{wolf_count}-Wolf Mated with {wolf2_count}-Wolf____________')
                            # action = True # works. still targets. but does not move. so fine!
                            break # ?activates else after eating.
                            #continue # no good. targets immediately another sheep. and activates else.
                        else:
                            print(f"----->1. Random >0.5. So they will fight. 50% probability of winning for both")
                            print(f"----->Stat: {wolf_count}-Wolf ({i}) before fighting with {wolf2_count}-Wolf ({j})")
                            if random.random() > 0.5:
                                print(f"------> Random > 0.5. So {wolf_count}-Wolf will win!")
                                gain = 0.5*j.store
                                i.store += gain
                                j.store -= gain
                                print(f"------> {wolf_count}-Wolf ({i}) won after fighting with {wolf2_count}-Wolf ({j})")
                            else:
                                print(f"------> Random < 0.5. So {wolf_count}-Wolf ({i}) will loose.")
                                lose = 0.5*i.store
                                i.store -= lose
                                j.store += lose
                                print(f"------> {wolf_count}-Wolf ({i}) lost after fighting with {wolf2_count}-Wolf ({j})")
                                # action = True
                            fight = True
                            print(f"Fight = {fight}")
                            print('_____________{wolf_count}-Wolf Fought with {wolf2_count}-Wolf____________')
                            break
                    else:
                        print(f"----->2. {wolf2_count}-Wolf has LESS than 500 store")
                        print('{wolf_count}-Wolf ({i}) and {wolf2_count}-Wolf ({j} will fight')
                        if random.random() > 0.25:
                            print(f"------> Random > 0.25. So {wolf_count}-Wolf will win 75% of {wolf2_count}-Wolf store.")
                            gain = 0.75*j.store
                            i.store += gain
                            j.store -= gain
                            print(f"------> {wolf_count}-Wolf ({i}) won after fighting with {wolf2_count}-Wolf ({j})")
                        else:
                            print(f"------> Random < 0.25. So {wolf_count}-Wolf will loose 50% store to {wolf2_count}-Wolf")
                            lose = 0.50*i.store #50% because i is the stronger wolf! so j will gain less.
                            i.store -= lose
                            j.store += lose
                            print(f"------> {wolf_count}-Wolf ({i}) lost after fighting with {wolf2_count}-Wolf ({j})")
                            # action = True
                        fight = True
                        print(f"Fight 2 = {fight}")
                        print('_____________{wolf_count}-Wolf Fought (2) with {wolf2_count}-Wolf____________')
                        break
                        # Need to add a boolean condition
                action = True # Need to check this!!!
            if action == True:
                #break
                print(f"---> action={action}, mated={breed}, fough={fight} for {wolf_count}-Wolf............")
                continue #( This works! it still targets but that's fine as long is it does not move!)
            elif closest_wolf != None:
                print(f"---> {wolf_count}-Wolf ({i}) before moving closer to CW-Wolf: ({closest_wolf })")
                i.y = (int((i.y + closest_wolf.y)/2)) % (len(environment))
                i.x = (int((i.x + closest_wolf.x)/2)) % (len(environment[0]))
                print(f"---> {wolf_count}-Wolf ({i}) after moving closer to CW-Wolf: ({closest_wolf })")
                print('..........{wolf_count}-Wolf moved closer CW+..........')   
            else: # No wolf. store >700
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) before normal moving")
                
                i.move()
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) after normal moving")
                print(f"....el2...... {wolf_count}-Wolf moved normally")
    print('________________Wolf Cycle Ends_________________')
        
    # for i in range(len(sheep)):
    #     sheep[i].move()
    #     sheep[i].eat()
    #     print(i, 'Sheep', sheep[i])
        
            
    # for i in range(len(wolves)):
    #     wolves[i].eat(proximity, i)
        
    # for i in range(len(wolves)):
    #     sheep_count = -1
    #     for j in sheep[:]:
    #         sheep_count += 1
    #         distance = af.Animal.dist_animals(wolves[i], j)
    #         # print(f"wolf{i}: {wolves[i].y},{wolves[i].x}, sheep{j}: {sheep[j].y},{sheep[j].x}, d={distance}")
    #         print(f"wolf {i}: {wolves[i].y},{wolves[i].x}, sheep: {sheep_count} {j.y},{j.x}, d={distance}")
    #         if distance < proximity:
    #             wolves[i].store += j.store
    #             j.store = 0
    #             print('Sheep eaten', sheep_count, j, 'by Wolf', i)
    #             sheep.remove(j)
    #             break


    
    plt.ylim(0, len(environment))
    plt.xlim(0, len(environment[0])) 
    plt.imshow(environment)
    for i in range(len(sheep)):
        plt.scatter(sheep[i].x, sheep[i].y, marker="p", color='white')
    for j in range(len(wolves)):
        plt.scatter(wolves[j].x, wolves[j].y, marker="v", color='black')


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


