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
    # for i in range(len(sheep)):
    sheep_count = -1
    sheep_index = 0 # To prevent breeding between same sheep or same pair!
    for i in sheep[:]:
        sheep_count += 1
        sheep_index += 1
        # print(sheep_count)
        # print(sheep_index)
        print('')
        print(f"-> ------------ {sheep_count} Sheep initialised -----------")
        min_dist = proximity*0.5 # coz sheep is a prey! wolves have higer field of vision!
        closest_wolf = None
        # print(min_dist) #
        # print(closest_wolf) #
        for j in range(len(wolves)): 
            print(f"--> {sheep_count}-Sheep looping with {j}-Wolf.") # To test if looping with all wolves!             
            # Calculate the distance between itself and all wolves.
            distance = af.Animal.dist_animals(i, wolves[j])
            # print(f"--> d={distance} for {i}-Sheep ({sheep[i]}) with {j}-Wolf ({wolves[j]})") #
            # If wolf/ves detected within min_dist, find the closest wolf (CW).
            if distance < min_dist:
                print(f"---> d<md+... {sheep_count}-Sheep noticed closest {j}-Wolf ...")
                min_dist = distance
                closest_wolf = wolves[j]
                print(f"---> {sheep_count}-Sheep ({i}) detected {j}-Wolf ({wolves[j]}) within d={min_dist}.")                
        if closest_wolf != None:
            # Need to adjust here based on store count and probability!
            print("-> CW FOUND.")
            print(f"-> Before {sheep_count}-Sheep ({i}) tries to run away from CW: ({closest_wolf}).")
            i.y = (i.y + (i.y - int((i.y + closest_wolf.y)/2))) % (len(environment))
            i.x = (i.x + (i.x - int((i.x + closest_wolf.x)/2))) % (len(environment[0]))
            print(f"-> After {sheep_count}-Sheep ({i}) tried to run away from CW ({closest_wolf}).")
            print(f"___________ {sheep_count} Sheep tried to run away from CW ___________ ")  
                
        elif closest_wolf == None:
            print(f"--> NO CW FOUND. No CS FOUND.")
            min_dist = proximity*0.5 # most prob not needed. will see later.
            # action = False
            breed = False
            share = False
            closest_sheep = None
            sheep2_count = -1
            for j in sheep[sheep_index:]:
                sheep2_count += 1
                print(f"--> {sheep_count}-Sheep looping with {sheep2_count}-Sheep.") # To test if looping with all wolves!             
                # Calculate the distance between itself and other sheep.
                distance = af.Animal.dist_animals(i, j)
                if (action_dist*2) < distance < min_dist: #for sheep, action_dist is twice that of wolves.
                    print('----> ---- (AD*2 < D < MD).')
                    min_dist = distance
                    closest_sheep = j
                    print(f"----> Min distance={min_dist} for {sheep_count}-Sheep ({i}) with {sheep2_count}-Sheep ({j}).")  
                elif distance <= (action_dist*2):
                    print(f"----> D <=AD. Sheep Breeding/Sharing proximity of {distance}(<={action_dist*2}) entered by {sheep_count}-Sheep ({i}) with CS {sheep2_count}-Sheep ({j}).")
                    min_energy = 500
                    if i.store and j.store > min_energy:
                        print(f"----->{sheep_count}-Sheep ({i}) and {sheep2_count}-Sheep ({j} has MORE than {min_energy} store. So they will breed if p>0.25")
                        if random.random() > 0.25: #75% chance of breeding!
                            print(f"------>1.A. Random >0.25. So the sheep will mate.")
                            print(f"------> {sheep_count}-Sheep ({i}) before mating with {sheep2_count}-Sheep ({j}).")
                            breeding_cost = ((i.store + j.store)/2)/2 # half of average.
                            i.store = breeding_cost
                            j.store = breeding_cost
                            print(f"------> {sheep_count}-Sheep ({i}) after mating with {sheep2_count}-Sheep ({j}).")
                            sheep.append(af.Sheep(animals, wolves, sheep, environment, x=(i.x+5), y=(i.y+5))) # x and y so that the new sheep appears closer!
                            breed = True
                            print(f"Breed = {breed}")
                            print(f"_____________ {sheep_count}-Sheep Mated with {sheep2_count}-Sheep ____________")
                            break
                        else:
                            print(f"------>1.B Random <0.25. So the sheep will not mate. But will share store to become average.")
                            print(f"------> {sheep_count}-Sheep ({i}) before sharing store (average) with {sheep2_count}-Sheep ({j})")
                            average = (i.store + j.store)/2
                            i.store = average
                            j.store = average
                            share = True
                            print(f"Share = {share}")
                            print(f"------> {sheep_count}-Sheep ({i}) after sharing store average({average}) with {sheep2_count}-Sheep ({j}).")
                            break
                    else:
                        # Print below to just show what is happening. Otherwise this else is not needed.
                        print(f"-----> {sheep_count}-Sheep ({i}) and {sheep2_count}-Sheep ({j} both DO NOT have MORE than {min_energy} store. So they will not breed")
                        print('No break here as I want it to loop through other sheep if i sheep (d<=ad) has >200 store.')
            if breed or share == True:  
                print(f"--->_______Mated={breed}, Shared={share} for {sheep_count}-Wolf__________")
                # Should add eat and move here?
                continue
            elif closest_sheep != None:
                print(f"->CS Found!")
                print(f"-> {sheep_count}-Sheep ({i}) before moving closer to CS-Sheep: ({closest_sheep}).")
                i.y = (int((i.y + closest_sheep.y)/2)) % (len(environment))
                i.x = (int((i.x + closest_sheep.x)/2)) % (len(environment[0]))
                print(f"-> {sheep_count}-Wolf ({i}) after moving closer to CS-Sheep: ({closest_sheep}).")
                print(f"___________ {sheep_count}-Sheep moved closer CS___________" )                   
            else:
                print(f"-> NO CW FOUND. No CS FOUND.")
                print(f"-> {sheep_count}-Sheep ({i}) before normally moving and eating.")
                i.move()
                i.eat()
                print(f"-> {sheep_count}-Sheep ({i}) after normally moving and eating.")
                print(f"___________ {sheep_count}-Sheep moved normally and ate ___________")
    print('')        
    print('________________Sheep Cycle Ends________________')
    print('________________Wolf Cycle Begins________________')
       
    wolf_count = -1
    wolf_index = 0 #to prevent comparison between same wolves!
    for i in wolves[:]:
        wolf_count += 1  
        wolf_index += 1
        print('')
        print(f"-> -----------{wolf_count}-Wolf initialised with ({i}) -----------")
        
        if i.store <= 500:
            print(f"--> {wolf_count}-Wolf has <=500 store ({i}). Tries to find food (sheep).")
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
                    # This works!
                    i.store += (j.store*(2/3)) # 2/3 eaten! 1/3 returned to env as can't eat everything!
                    env_rcv = (j.store*(1/3)) # env receives 1/3 store!
                    i.environment[i.y][i.x] += env_rcv 
                    j.store = 0
                    print(f"----> {wolf_count}-Wolf ({i}) after eating {sheep_count}-Sheep ({j}). Env received ({env_rcv})")
                    sheep.remove(j)
                    eaten = True # works. still targets. but does not move. so fine!
                    break # works! goes to eaten true!
                    # continue # no good. targets immediately another sheep. and activates else.
                elif action_dist < distance < min_dist:
                    print(f"----> action_dist < distance < min_dist")
                    min_dist = distance
                    closest_sheep = j
                    print(f"----> Min Distance = {min_dist} for {wolf_count}-Wolf ({i}) with {sheep_count}-Sheep ({j})")
                    print('....elif adm ends....')
            if eaten == True:
                #break
                print(f"---> ___________Eaten={eaten}. {wolf_count}-Wolf one ate CS {sheep_count}__________")
                continue # This works!
                
            elif closest_sheep != None:
                print(f"-> CS Found!")
                print(f"--> {wolf_count}-Wolf ({i}) before moving closer to  CS-Sheep ({closest_sheep })")
                i.y = (int((i.y + closest_sheep.y)/2)) % (len(environment))
                i.x = (int((i.x + closest_sheep.x)/2)) % (len(environment[0]))
                print(f"--> {wolf_count}-Wolf ({i}) after moving closer to Sheep ({closest_sheep })")
                print(f"..........{wolf_count}-Wolf moved closer to CS+..........")           
            else: #no sheep and store <500
                print(f"-> No CS found and store <500!")
                print(f"-->else1 begins: {wolf_count}-Wolf ({i}) before normal moving")
                i.move()
                print(f"-->else1 ends: {wolf_count}-Wolf ({i}) after normal moving")
                print(f"....el1......{wolf_count}-Wolf moved normally..........")
        elif i.store > 500: # Wolf tries to breed / fight. Can also just write else.
            print(f"--> {wolf_count}-Wolf has >500 store ({i})")
            min_dist = proximity
            # action = False
            fight = False
            breed = False
            closest_wolf = None
            wolf2_count = -1
            for j in wolves[wolf_index:]: # so that action is not duplicated for same wolf or same pair.
                wolf2_count += 1
                print(f"---> {wolf_count}-Wolf looping with {wolf2_count}-Wolf")
                distance =  af.Animal.dist_animals(i, j)
                if action_dist < distance < min_dist: 
                    print('----> (AD2 < D < MD).')
                    min_dist = distance
                    closest_sheep = j
                    print(f"----> Min distance={min_dist} for {wolf_count}-Wolf ({i}) with {wolf2_count}-Wolf ({j})")  
                elif distance <= action_dist:
                    print(f"----> d<=ad. breeding/fight proximity of {distance}(<={action_dist}) entered by {wolf_count}-Wolf ({i}) with CW {wolf2_count}-Wolf ({j}).")
                    if j.store > 500:
                        print(f"----->{wolf2_count}-Wolf ({j} has MORE than 500 store. So they will either breed or fight. 50% probability each.")
                        if random.random() < 0.5: #50% chance of meeting a female!
                            print(f"------>1.A. Random <0.5. So the wolves will mate.")
                            print(f"------> {wolf_count}-Wolf ({i}) before mating with {wolf2_count}-Wolf ({j})")
                            # This works!
                            breeding_cost = ((i.store + j.store)/2)/2 # half of average.
                            # i.store = average - 200 # 200 is energy for mating.
                            # j.store = average - 200 # They will share average energy - 200 energy for mating.
                            i.store = breeding_cost
                            j.store = breeding_cost
                            print(f"------> {wolf_count}-Wolf ({i}) after mating with {wolf2_count}-Wolf ({j})")
                            # wolves.append(j) # Added new wolf to the list.
                            wolves.append(af.Wolf(animals, wolves, sheep, environment)) # need to add x and y to set the value!
                            breed = True
                            print(f"Breed = {breed}")
                            print(f"_____________{wolf_count}-Wolf Mated with {wolf2_count}-Wolf____________")
                            # action = True # works. still targets. but does not move. so fine!
                            break # ?activates else after eating.
                            #continue # no good. targets immediately another sheep. and activates else.
                        else:
                            print(f"----->1.B. Random >0.5. So they will fight. 50% probability of winning for both")
                            print(f"----->Stat: {wolf_count}-Wolf ({i}) before fighting with {wolf2_count}-Wolf ({j})")
                            if random.random() > 0.5:
                                print(f"------>1.B.i. Random > 0.5. So {wolf_count}-Wolf will win 50% store of {wolf2_count}-Wolf.")
                                gain = (j.store/2)
                                print('gain', gain)
                                i.store += gain
                                print('i.store', i.store)
                                j.store -= gain
                                print('j.store', j.store)
                                print(f"------> {wolf_count}-Wolf ({i}) won after fighting with {wolf2_count}-Wolf ({j})")
                            else:
                                print(f"------>1.B.ii. Random < 0.5. So {wolf_count}-Wolf ({i}) will loose 50% store to {wolf2_count}-Wolf.")
                                lose = (i.store/2)
                                print('lose', lose)
                                i.store -= lose
                                print('i.store', i.store)
                                j.store += lose
                                print('j.store', j.store)
                                print(f"------> {wolf_count}-Wolf ({i}) lost after fighting with {wolf2_count}-Wolf ({j})")
                                # action = True
                            fight = True
                            print(f"Fight 1= {fight}")
                            print(f"_____________{wolf_count}-Wolf Fought-(1) with {wolf2_count}-Wolf____________")
                            break
                    else:
                        print(f"----->2.A. {wolf2_count}-Wolf has LESS than 500 store")
                        print(f"----->{wolf_count}-Wolf ({i}) and {wolf2_count}-Wolf ({j} will fight")
                        # This works! 
                        if random.random() > 0.50:
                            # print(f"------>2.A.i. Random > 0.25. So {wolf_count}-Wolf will win 75% of {wolf2_count}-Wolf store.")
                            print(f"------>2.A.i. Random > 0.50. So {wolf_count}-Wolf will win 50% of {wolf2_count}-Wolf store.")
                            gain = (j.store*0.50)
                            i.store += gain
                            j.store -= gain
                            print(f"------> {wolf_count}-Wolf ({i}) won after fighting with {wolf2_count}-Wolf ({j})")
                        else:
                            # print(f"------>2.A.ii. Random < 0.25. So {wolf_count}-Wolf will loose 25% store to {wolf2_count}-Wolf")
                            print(f"------>2.A.ii. Random < 0.50. So {wolf_count}-Wolf will loose 50% store to {wolf2_count}-Wolf")
                            lose = (i.store*0.50)
                            i.store -= lose
                            j.store += lose
                            print(f"------> {wolf_count}-Wolf ({i}) lost after fighting with {wolf2_count}-Wolf ({j})")
                            # action = True
                        fight = True
                        print(f"Fight 2 = {fight}")
                        print(f"_____________{wolf_count}-Wolf Fought-(2) with {wolf2_count}-Wolf____________")
                        break
                        
            if breed or fight == True:   
                # action = True
                print(f"--->_______Mated={breed}, Fought={fight} for {wolf_count}-Wolf__________")
                continue
            
            # if action == True:
            #     #break
            #     print(f"---> action={action}, mated={breed}, fough={fight} for {wolf_count}-Wolf............")
            #     continue #( This works! it still targets but that's fine as long is it does not move!)
            elif closest_wolf != None:
                print(f"->CW Found!")
                print(f"-> {wolf_count}-Wolf ({i}) before moving closer to CW-Wolf: ({closest_wolf}).")
                i.y = (int((i.y + closest_wolf.y)/2)) % (len(environment))
                i.x = (int((i.x + closest_wolf.x)/2)) % (len(environment[0]))
                print(f"-> {wolf_count}-Wolf ({i}) after moving closer to CW-Wolf: ({closest_wolf}).")
                print(f"..........{wolf_count}-Wolf moved closer CW+..........")   
            else: # No wolf. store >700
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) before normal moving.")
                i.move()
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) after normal moving.")
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
