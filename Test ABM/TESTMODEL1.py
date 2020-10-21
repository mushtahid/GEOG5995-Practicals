# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 09:26:33 2020

@author: Mushtahid
"""
import sys 
import TESTAF1 as af
import tkinter
import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation
import random
# random.seed(10)
import csv
import requests
import bs4

stdoutOrigin=sys.stdout 
sys.stdout = open("log.txt", "w")



# Scrape web data to initialise model
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
# print(td_ys)
# print(td_xs)

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
    y = int(td_ys[i].text)
    x = int(td_xs[i].text)
    sheep.append(af.Sheep(animals, wolves, sheep, environment, y, x)) 
print('No sheep', len(sheep))

for i in range(no_wolves):
    y = int(td_ys[-i].text)*3 #interesting!
    x = int(td_xs[-i].text)*3
    wolves.append(af.Wolf(animals, wolves, sheep, environment, y, x))
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
    
    random.shuffle(sheep)
    random.shuffle(wolves)
     

### NEED TO ADJUST THE PRINT TAGS LATER   
    sheep_count = -1
    sheep_index = 0 # Prevent breeding between same sheep/same pair.
    for i in sheep[:]:
        sheep_count += 1
        sheep_index += 1
        # print(sheep_count)
        # print(sheep_index)
        print('')
        print(f"-> ------------ {sheep_count}-Sheep initialised with ({i}) -----------")
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
            print(f"--> Before {sheep_count}-Sheep ({i}) tries to run away from CW: ({closest_wolf}).")
            i.y = i.y + (i.y - int((i.y + closest_wolf.y)/2))
            i.x = i.x + (i.x - int((i.x + closest_wolf.x)/2))
            i.boundary_conditons()
            print(f"--> After {sheep_count}-Sheep ({i}) tried to run away from CW ({closest_wolf}).")
            print(f"___________ {sheep_count} Sheep tried to run away from CW ___________ ")  
            # for j to if CW+ checked    
        elif closest_wolf == None:
            print(f"-> NO CW FOUND. Will try to either (if energy allows: find CS to move closer+eat OR breed/share) OR (move/eat normally if low energy).")
            min_dist = proximity*0.5 # most prob not needed. will see later.
            # action = False
            breed = False
            fail_breed = False
            share = False
            closest_sheep = None
            sheep2_count = -1
            min_energy = 600
            # if e>600 tries to find CS
            if i.store > min_energy:
                print(f"->{sheep_count}-Sheep has Store > Min_ernergy({min_energy}) ({i}).")
                for j in sheep[sheep_index:]:
                    sheep2_count += 1
                    print(f"--> {sheep_count}-Sheep looping with {sheep2_count}-Sheep.") # To test if looping with i+1 sheep!             
                    # Calculate the distance between itself and other sheep.
                    distance = af.Animal.dist_animals(i, j)
                    if action_dist < distance < min_dist:
                        print('----> ---- (AD < D < MD).')
                        min_dist = distance
                        closest_sheep = j
                        print(f"----> Min distance={min_dist} for {sheep_count}-Sheep ({i}) with {sheep2_count}-Sheep ({j}).")  
                    elif distance <= action_dist:
                        breeding_chance = 0.50
                        print(f"----> D <=AD. Sheep Breeding/Sharing proximity of {distance}(<={action_dist}) entered by CS {sheep_count}-Sheep ({i}) with CS {sheep2_count}-Sheep ({j}).")
                        if j.store > min_energy: # Sheep j also has to have store >600 to have chance of breeding
                            print(f"----->{sheep_count}-Sheep ({i}) and CS {sheep2_count}-Sheep ({j} have > Min_energy ({min_energy}) store. So they will try breeding if p>{breeding_chance}")
                            breeding_cost = ((i.store + j.store)/2)/2 # half of average.
                            if random.random() > breeding_chance:
                                print(f"------>1.A. Random >{breeding_chance}. So the sheep will breed.")
                                print(f"------> {sheep_count}-Sheep ({i}) before breeding with CS {sheep2_count}-Sheep ({j}).")
                                i.store = breeding_cost
                                j.store = breeding_cost
                                sheep.append(af.Sheep(animals, wolves, sheep, environment, y=(i.y+10), x=(i.x+10))) # x and y so that the new sheep appears closer!
                                # i.boundary_conditons()
                                breed = True
                                print(f"------> Sheep Breed = {breed}")
                                print(f"------> {sheep_count}-Sheep ({i}) after breeding with CS {sheep2_count}-Sheep ({j}).")
                                print(f"_____________ {sheep_count}-Sheep Mated SUCCESSFULLY with CS {sheep2_count}-Sheep ____________")
                                break
                            else:
                                print(f"------>1.B Random <{breeding_chance}. So the breeding will fail.")
                                print(f"------> {sheep_count}-Sheep ({i}) before failed breeding with CS {sheep2_count}-Sheep ({j})")
                                # average = (i.store + j.store)/2
                                i.store = breeding_cost # breeding attempted. just was not successful!
                                j.store = breeding_cost
                                fail_breed = True
                                print(f"------> Failed Sheep Breeding = {fail_breed}")
                                print(f"------> {sheep_count}-Sheep ({i}) after failed breeding with CS {sheep2_count}-Sheep ({j}).")
                                print(f"_____________ {sheep_count}-Sheep Fail Mated with CS {sheep2_count}-Sheep ____________")
                                break
                        else:
                            print(f"-----> {sheep_count}-Sheep ({i}) and CS {sheep2_count}-Sheep ({j} will not mate as CS {sheep2_count}-Sheep store <{min_energy}. They will share resource to become average.")
                            average = (i.store + j.store)/2
                            i.store = average
                            j.store = average
                            share = True
                            print(f"-----> Shared resources = {share}")
                            print(f"-----> {sheep_count}-Sheep ({i}) and CS {sheep2_count}-Sheep ({j}) after sharing resources!")
                            print(f"_____________ {sheep_count}-Sheep and CS {sheep2_count}-Sheep shared resources ____________")
                            break
                if breed or fail_breed or share == True:  
                    print(f"_______ Breeding={breed}, Failed breeding={fail_breed}, Share={share} for {sheep_count}-Sheep __________")
                    # Should add eat and move here? No i guess because they came <ad
                    continue
                elif closest_sheep != None:
                    # Sheep likes to stay in a herd. So stay close and eats too!
                    print(f"->CS Found!")
                    print(f"-> {sheep_count}-Sheep ({i}) before moving closer (while eating) to CS-Sheep: ({closest_sheep}).")
                    i.y = (int((i.y + closest_sheep.y)/2))
                    i.x = (int((i.x + closest_sheep.x)/2))
                    i.boundary_conditons()
                    i.eat() # This should produce interesting results!
                    print(f"-> {sheep_count}-Wolf ({i}) after moving closer (while eating) to CS-Sheep: ({closest_sheep}).")
                    print(f"___________ {sheep_count}-Sheep moved closer CS___________" )                   
                else:
                    print(f"-> NO CS Found.")
                    print(f"-> {sheep_count}-Sheep ({i}) before normally moving and eating.")
                    i.move()
                    i.eat()
                    print(f"-> {sheep_count}-Sheep ({i}) after normally moving and eating.")
                    print(f"___e1________ {sheep_count}-Sheep moved normally and ate ___________")
            
            else: # if i energey < {min_energy}
                print(f"->{sheep_count}-Sheep has Store < Min_ernergy({min_energy}) ({i}). Will move normally and eat")
                print(f"-->{sheep_count}-Sheep ({i}) before normal moving and eating")
                i.move()
                i.eat()
                print(f"-->{sheep_count}-Sheep ({i}) after normal moving and eating")
                print(f"___e2________ {sheep_count}-Sheep moved normally and ate ___________")
                # wolf checked. none found. energy <600 checked.
        
        print('')        
    print('________________Sheep Cycle Ends________________')
    print('________________Wolf Cycle Begins________________')
       
    wolf_count = -1
    wolf_index = 0 #to prevent comparison between same wolves!
    for i in wolves[:]:
        wolf_count += 1  
        wolf_index += 1
        min_energy = 500
        bf_e = 0.5
        print('')
        print(f"---------{wolf_count}-Wolf initialised with ({i}) --------")
        
        if i.store <= min_energy or (i.store > min_energy and ((bf_e/2) <= random.random() < bf_e)):
            # print()
            if i.store <= min_energy:
                print(f"--> {wolf_count}-Wolf has <=Min_energy({min_energy}) store ({i}). Tries to find food (sheep).")
            else:
                print(f"--> {wolf_count}-Wolf has >Min_energy({min_energy}) store ({i}) and {bf_e/2} <= random.random() < {bf_e}. Tries to find food (sheep).")
            # print(f"--> {wolf_count}-Wolf has <=Min_energy({min_energy}) store ({i}). Tries to find food (sheep).")
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
                    print(f"----> {wolf_count}-Wolf ({i}) before eating CS {sheep_count}-Sheep ({j})")
                    i.store += (j.store*(4/5)) # 4/5 eaten! 1/5 returned to env as can't eat everything!
                    env_rcv = (j.store*(1/5)) # env receives 1/5 store!
                    i.environment[i.y][i.x] += env_rcv 
                    j.store = 0
                    print(f"----> {wolf_count}-Wolf ({i}) after eating CS {sheep_count}-Sheep ({j}). Env received ({env_rcv})")
                    sheep.remove(j)
                    eaten = True 
                    break
                elif action_dist < distance < min_dist:
                    print(f"----> action_dist({action_dist}) < distance({distance}) < min_dist({min_dist})")
                    min_dist = distance
                    closest_sheep = j
                    print(f"----> Min Distance = {min_dist} for {wolf_count}-Wolf ({i}) with {sheep_count}-Sheep ({j})")
            if eaten == True:
                print(f"___________ Eaten={eaten}. {wolf_count}-Wolf one ate CS {sheep_count}-Sheep__________")
                continue # This works!    
            elif closest_sheep != None:
                print(f"-> CS Found!")
                print(f"--> {wolf_count}-Wolf ({i}) before moving closer to  CS ({closest_sheep })")
                i.y = (int((i.y + closest_sheep.y)/2))
                i.x = (int((i.x + closest_sheep.x)/2))
                i.boundary_conditons()
                print(f"--> {wolf_count}-Wolf ({i}) after moving closer to CS ({closest_sheep })")
                print(f"___________ {wolf_count}-Wolf moved closer to CS___________")           
            else: #no sheep
                print(f"-> No CS found!")
                print(f"-->else1 begins: {wolf_count}-Wolf ({i}) before normal moving")
                i.move()
                print(f"-->else1 ends: {wolf_count}-Wolf ({i}) after normal moving")
                print(f"....el1___________ {wolf_count}-Wolf moved normally___________")
                
        elif i.store > min_energy and random.random() >= bf_e: 
            print(f"--> {wolf_count}-Wolf has > {min_energy} store ({i}) and Random >= {bf_e}. so will try to find CW to move closer or breed/fight if within AD({action_dist}).")                     
            min_dist = proximity
            # action = False
            fight = False
            breed = False
            fail_breed = False
            closest_wolf = None
            wolf2_count = -1
            for j in wolves[wolf_index:]: # so that action is not duplicated for same wolf or same pair.
                wolf2_count += 1
                print(f"---> {wolf_count}-Wolf looping with {wolf2_count}-Wolf")
                distance =  af.Animal.dist_animals(i, j)
                if action_dist < distance < min_dist: 
                    print('----> (AD2 < D < MD).')
                    min_dist = distance
                    closest_wolf = j
                    print(f"----> Min distance={min_dist} for {wolf_count}-Wolf ({i}) with {wolf2_count}-Wolf ({j})")  
                elif distance <= action_dist:
                    print(f"----> d<=ad. breeding/fight roximity of {distance}(<={action_dist}) entered by {wolf_count}-Wolf ({i}) with CW {wolf2_count}-Wolf ({j}).")
                    if j.store > min_energy:
                        print(f"-----> CW {wolf2_count}-Wolf ({j} has > {min_energy} store. So they will try breeding. {bf_e*100}% probability breeding successfully.")
                        breeding_cost = ((i.store + j.store)/2)/2 # half of average.
                        if random.random() > bf_e:
                            print(f"------>1.A. Random >{bf_e}. So the wolves will mate.")
                            print(f"------> {wolf_count}-Wolf ({i}) before mating with CW {wolf2_count}-Wolf ({j})")
                            i.store = breeding_cost
                            j.store = breeding_cost
                            wolves.append(af.Wolf(animals, wolves, sheep, environment, y=(i.y+5), x=(i.x+5)))
                            breed = True
                            print(f"------> Breed = {breed}")
                            print(f"------> {wolf_count}-Wolf ({i}) after mating with CW {wolf2_count}-Wolf ({j})")
                            print(f"_____________ {wolf_count}-Wolf Mated SUCCESSFULLY with CW {wolf2_count}-Wolf ____________")
                        else:
                            print(f"----->1.B. Random <{bf_e}. So breeding will not be successful.")
                            print(f"----->{wolf_count}-Wolf ({i}) before fail breeding with CW {wolf2_count}-Wolf ({j})")
                            i.store = breeding_cost
                            j.store = breeding_cost  
                            fail_breed = True
                            print(f"------> Fail Breeding = {fail_breed}")
                            print(f"_____________ {wolf_count}-Wolf ({i}) after fail breeding with CW {wolf2_count}-Wolf ({j})")
                        break
                    else:
                        print(f"----->2.A. CW {wolf2_count}-Wolf has < than {min_energy} store")
                        print(f"------>{wolf_count}-Wolf ({i}) will FIGHT CW {wolf2_count}-Wolf ({j}) & move")
                        # This works! 
                        if random.random() > bf_e:
                            # print(f"------>2.A.i. Random > 0.25. So {wolf_count}-Wolf will win 75% of {wolf2_count}-Wolf store.")
                            print(f"------>2.A.i. Random > {bf_e}. So {wolf_count}-Wolf will win {bf_e*100}% of CW {wolf2_count}-Wolf store.")
                            gain = (j.store*bf_e)
                            i.store += gain
                            j.store -= gain
                            i.move() # MOVE ADDED
                            print(f"------> {wolf_count}-Wolf ({i}) won+moved after fighting with CW {wolf2_count}-Wolf ({j})")
                        else:
                            # print(f"------>2.A.ii. Random < 0.25. So {wolf_count}-Wolf will loose 25% store to {wolf2_count}-Wolf")
                            print(f"------>2.A.ii. Random < {bf_e}. So {wolf_count}-Wolf will loose {bf_e*100}% store to CW {wolf2_count}-Wolf")
                            lose = (i.store*bf_e)
                            i.store -= lose
                            j.store += lose
                            i.move() # MOVE ADDED
                            print(f"------> {wolf_count}-Wolf ({i}) lost+moved after fighting with CW {wolf2_count}-Wolf ({j})")
                            # action = True
                        fight = True
                        print(f"------> Fight = {fight}")
                        print(f"_____________ {wolf_count}-Wolf Fought-(2) with CW {wolf2_count}-Wolf ____________")
                        break
            if breed or fail_breed or fight == True:   
                print(f"_______ Breed={breed}, Failed Breed={fail_breed}, Fought={fight} for {wolf_count}-Wolf __________")
                continue
            elif closest_wolf != None:
                print(f"->CW Found!")
                print(f"-> {wolf_count}-Wolf ({i}) before moving closer to CW-Wolf: ({closest_wolf}).")
                i.y = (int((i.y + closest_wolf.y)/2))
                i.x = (int((i.x + closest_wolf.x)/2))
                i.boundary_conditons()
                print(f"-> {wolf_count}-Wolf ({i}) after moving closer to CW-Wolf: ({closest_wolf}).")
                print(f"_______ {wolf_count}-Wolf moved closer CW+_______")   
            else: # No CW. E>min_energy and p>bf_e
                print(f"-> No CW found. although store >{min_energy} and p>={bf_e}!")
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) before normal moving.")
                i.move()
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) after normal moving.")
                print(f".... el2 _______  {wolf_count}-Wolf moved normally _______ ")
        else: # if and elif not satisfied
            # Better yet. Make this resting for the wolves. And put the above idea with <500 if.
            print(f"--> if and elif not satisfied")
            print(f"--> {wolf_count}-Wolf has > Min_energy({min_energy}) store ({i}) but Random < bf_e/2({bf_e/2}). So will move normally.")
            print(f"--->else3 begins: {wolf_count}-Wolf ({i}) before normal moving.")
            i.move()
            print(f"--->else3 begins: {wolf_count}-Wolf ({i}) after normal moving.")
            print(f"....e3_______ {wolf_count}-Wolf moved normally_______")
    
    
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

sys.stdout.close()
sys.stdout=stdoutOrigin
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
    
    
    
    
    
    
    
    #     elif i.store > 500: # Wolf tries to breed / fight. Can also just write else.
    #         print(f"--> {wolf_count}-Wolf has >500 store ({i})")
    #         min_dist = proximity
    #         # action = False
    #         fight = False
    #         breed = False
    #         closest_wolf = None
    #         wolf2_count = -1
    #         for j in wolves[wolf_index:]: # so that action is not duplicated for same wolf or same pair.
    #             wolf2_count += 1
    #             print(f"---> {wolf_count}-Wolf looping with {wolf2_count}-Wolf")
    #             distance =  af.Animal.dist_animals(i, j)
    #             if action_dist < distance < min_dist: 
    #                 print('----> (AD2 < D < MD).')
    #                 min_dist = distance
    #                 closest_sheep = j
    #                 print(f"----> Min distance={min_dist} for {wolf_count}-Wolf ({i}) with {wolf2_count}-Wolf ({j})")  
    #             elif distance <= action_dist:
    #                 print(f"----> d<=ad. breeding/fight proximity of {distance}(<={action_dist}) entered by {wolf_count}-Wolf ({i}) with CW {wolf2_count}-Wolf ({j}).")
    #                 if j.store > 500:
    #                     print(f"----->{wolf2_count}-Wolf ({j} has MORE than 500 store. So they will either breed or fight. 50% probability each.")
    #                     if random.random() < 0.5: #50% chance of meeting a female!
    #                         print(f"------>1.A. Random <0.5. So the wolves will mate.")
    #                         print(f"------> {wolf_count}-Wolf ({i}) before mating with {wolf2_count}-Wolf ({j})")
    #                         # This works!
    #                         breeding_cost = ((i.store + j.store)/2)/2 # half of average.
    #                         # i.store = average - 200 # 200 is energy for mating.
    #                         # j.store = average - 200 # They will share average energy - 200 energy for mating.
    #                         i.store = breeding_cost
    #                         j.store = breeding_cost
    #                         print(f"------> {wolf_count}-Wolf ({i}) after mating with {wolf2_count}-Wolf ({j})")
    #                         # wolves.append(j) # Added new wolf to the list.
    #                         wolves.append(af.Wolf(animals, wolves, sheep, environment, y=(i.y+10), x=(i.x+10))) # need to add x and y to set the value!
    #                         breed = True
    #                         print(f"Breed = {breed}")
    #                         print(f"_____________{wolf_count}-Wolf Mated with {wolf2_count}-Wolf____________")
    #                         # action = True # works. still targets. but does not move. so fine!
    #                         break # ?activates else after eating.
    #                         #continue # no good. targets immediately another sheep. and activates else.
    #                     else:
    #                         print(f"----->1.B. Random >0.5. So they will fight. 50% probability of winning for both")
    #                         print(f"----->Stat: {wolf_count}-Wolf ({i}) before fighting with {wolf2_count}-Wolf ({j})")
    #                         if random.random() > 0.5:
    #                             print(f"------>1.B.i. Random > 0.5. So {wolf_count}-Wolf will win 50% store of {wolf2_count}-Wolf.")
    #                             gain = (j.store/2)
    #                             print('gain', gain)
    #                             i.store += gain
    #                             print('i.store', i.store)
    #                             j.store -= gain
    #                             print('j.store', j.store)
    #                             print(f"------> {wolf_count}-Wolf ({i}) won after fighting with {wolf2_count}-Wolf ({j})")
    #                         else:
    #                             print(f"------>1.B.ii. Random < 0.5. So {wolf_count}-Wolf ({i}) will loose 50% store to {wolf2_count}-Wolf.")
    #                             lose = (i.store/2)
    #                             print('lose', lose)
    #                             i.store -= lose
    #                             print('i.store', i.store)
    #                             j.store += lose
    #                             print('j.store', j.store)
    #                             print(f"------> {wolf_count}-Wolf ({i}) lost after fighting with {wolf2_count}-Wolf ({j})")
    #                             # action = True
    #                         fight = True
    #                         print(f"Fight 1= {fight}")
    #                         print(f"_____________{wolf_count}-Wolf Fought-(1) with {wolf2_count}-Wolf____________")
    #                         break
    #                 else:
    #                     print(f"----->2.A. {wolf2_count}-Wolf has LESS than 500 store")
    #                     print(f"----->{wolf_count}-Wolf ({i}) and {wolf2_count}-Wolf ({j} will fight")
    #                     # This works! 
    #                     if random.random() > 0.50:
    #                         # print(f"------>2.A.i. Random > 0.25. So {wolf_count}-Wolf will win 75% of {wolf2_count}-Wolf store.")
    #                         print(f"------>2.A.i. Random > 0.50. So {wolf_count}-Wolf will win 50% of {wolf2_count}-Wolf store.")
    #                         gain = (j.store*0.50)
    #                         i.store += gain
    #                         j.store -= gain
    #                         print(f"------> {wolf_count}-Wolf ({i}) won after fighting with {wolf2_count}-Wolf ({j})")
    #                     else:
    #                         # print(f"------>2.A.ii. Random < 0.25. So {wolf_count}-Wolf will loose 25% store to {wolf2_count}-Wolf")
    #                         print(f"------>2.A.ii. Random < 0.50. So {wolf_count}-Wolf will loose 50% store to {wolf2_count}-Wolf")
    #                         lose = (i.store*0.50)
    #                         i.store -= lose
    #                         j.store += lose
    #                         print(f"------> {wolf_count}-Wolf ({i}) lost after fighting with {wolf2_count}-Wolf ({j})")
    #                         # action = True
    #                     fight = True
    #                     print(f"Fight 2 = {fight}")
    #                     print(f"_____________{wolf_count}-Wolf Fought-(2) with {wolf2_count}-Wolf____________")
    #                     break
                        
    #         if breed or fight == True:   
    #             # action = True
    #             print(f"--->_______Mated={breed}, Fought={fight} for {wolf_count}-Wolf__________")
    #             continue
            
    #         # if action == True:
    #         #     #break
    #         #     print(f"---> action={action}, mated={breed}, fough={fight} for {wolf_count}-Wolf............")
    #         #     continue #( This works! it still targets but that's fine as long is it does not move!)
    #         elif closest_wolf != None:
    #             print(f"->CW Found!")
    #             print(f"-> {wolf_count}-Wolf ({i}) before moving closer to CW-Wolf: ({closest_wolf}).")
    #             i.y = (int((i.y + closest_wolf.y)/2))
    #             i.x = (int((i.x + closest_wolf.x)/2))
    #             i.boundary_conditons()
    #             print(f"-> {wolf_count}-Wolf ({i}) after moving closer to CW-Wolf: ({closest_wolf}).")
    #             print(f"..........{wolf_count}-Wolf moved closer CW+..........")   
    #         else: # No wolf. store >700
    #             print(f"--->else2 begins: {wolf_count}-Wolf ({i}) before normal moving.")
    #             i.move()
    #             print(f"--->else2 begins: {wolf_count}-Wolf ({i}) after normal moving.")
    #             print(f"....el2...... {wolf_count}-Wolf moved normally")
    # print('________________Wolf Cycle Ends_________________')
