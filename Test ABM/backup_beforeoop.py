# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 19:44:14 2020

@author: Md Mushtahid Salam
email: mushtahid@gmail.com
"""
# Import modules
import sys # To print the output in a seperate text file
import beforeoopaf as af # Import the agentframework
import tkinter # To use for the GUI
# For plotting and displaying environment and animals.
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation
import random # To randomize things!
random.seed(10) # Uncomment to debug the model
import csv # To read and write data
import requests # To scrape web data
import bs4 # To scrape web data

# Print out the output in a text file
# Better for debuggin the code as it can be searched easily using keywords!
stdoutOrigin=sys.stdout 
sys.stdout = open("log2.txt", "w")

# Scrape web data to find x and y values for the sheep!
r = requests.get('http://bit.ly/GeogLeedsAFData')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
# print(td_ys)
# print(td_xs)

# Set up variables
environment = []
animals = []
sheep = []
wolves = []
no_sheep = 15
no_wolves = 5

no_iterations = 100 # Number of times the animation will run
it_no = -1 # No of iterations
proximity = 50 # the range of vision of the animals
action_dist = 5 # Proximity within which animals can interact, eg breed etc. 
no_animals = no_sheep + no_wolves # Delete
# Set up plot size and axes
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

# Read environment data from a text file.
with open('in.txt', newline='') as f:
    env_reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in env_reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)

# Initialise sheep
for i in range(no_sheep):
# Multiply x and y to make them more spread out. However, I did not
# as the sheep should stay in a herd. So makes sense for them to appear 
# closer within a grid of 100X100 as assigned by the webdata!
    y = int(td_ys[i].text) 
    x = int(td_xs[i].text)
    sheep.append(af.Sheep(animals, wolves, sheep, environment, y, x)) 
print('Initial number of  sheep: ', len(sheep))

# Initialise wolves
for i in range(no_wolves):
    y = None #int(td_ys[-i].text)*3 #interesting!
    x = None #int(td_xs[-i].text)*3
    wolves.append(af.Wolf(animals, wolves, sheep, environment, y, x))
print('Initial number of  wolves:', len(wolves))
        
# Set up update/frames for animation
def update(frame_number):
    fig.clear() # Clear the figure from previous iteration!
    global it_no
    it_no += 1
    print('') # Add a space between two iteration printouts!
    print(f"*************** ITERATION NUMBER {it_no} ************")
    
    # Randomly shuffle the order of initialisation for the animals
    # at each iteration so that everyone gets a fair shot at 
    # whatever their action is (eating/breeding/mating/fighting etc.)
    random.shuffle(sheep)
    random.shuffle(wolves)
    
    # sheep_count tracks the current sheep (i) via it's index value.
    sheep_count = -1
    # sheep_index tracks the other sheep (j) with which  the current sheep 
    # interacts with via their index value. Used to prevent the current sheep 
    # from interacting with itself and prevent interaction of the same pair
    # in the same iteration.
    sheep_index = 0
    # slice [:] is used in for loop because sheep may breed with each other.
    for i in sheep[:]:
        sheep_count += 1 # Increase by 1 to assign the i sheep it's index.
        sheep_index += 1 # Increase by 1 to use as the start index 
                         # when comapring with other sheep.
        # print(sheep_count)
        # print(sheep_index)
        print('')
        print(f"-> ----- {sheep_count}-Sheep initialised with ({i}) ------")
        # Min_dist for sheep is half of proximity as sheep is a prey! 
        # Wolves have higer field of vision, so they have access to full
        # proximity distance!
        min_dist = proximity*0.5
        # closest_wolf targets and tracks the closest wolf to run away from!
        closest_wolf = None
        # print(min_dist)
        # print(closest_wolf)
        
        # Actions for sheep: check for close wolves (CW) within min_dist. 
        # If found, run away. While running away it does not eat.
        # If no CW. Looks for close sheep (CS) if it has min_energy to move 
        # closer/breed/share. While moving closer it eats as well. If no CS
        # found but has min_energy it moves randomly and eats. If it does not 
        # have min_energy then it moves randomly and eats.
        
        # For j loop below, range(len(wolves)) is used. Slice of wolves is 
        # not used while looping with sheep as the wolves will not mate with 
        # sheep to increase the number of wolves. range(no_wolves) is not used
        # as no_wolves represents inital wolf number and the wolves may breed
        # to increase their numbers, and so would fail the model.
        for j in range(len(wolves)):
            # Print below tests if current sheep is looping with all wolves!
            print(f"--> {sheep_count}-Sheep looping with {j}-Wolf.")             
            # Calculate the distance between itself and all wolves.
            distance = af.Animal.dist_animals(i, wolves[j])
            # print(f"--> distance={distance} for {i}-Sheep ({sheep[i]}) with"
            #       f"{j}-Wolf ({wolves[j]})")
            
            # If wolf(ves) detected within min_dist, find the 
            # closest wolf (CW).
            if distance < min_dist: # d<md+
                print(f"--->d<md+...{sheep_count}-Sheep noticed "
                      f"closest {j}-Wolf ...") # This may be commented off!
                min_dist = distance # Assign the new min_dist
                closest_wolf = wolves[j] # Assign the new CW
                print(f"---> {sheep_count}-Sheep ({i}) detected {j}-Wolf "
                      f"({wolves[j]}) within d={min_dist}.")                
        
        # If CW found, try to run away!
        if closest_wolf != None:
            # The algorithm may be improved here based on store 
            # and probability
            print("-> CW FOUND.")
            print(f"--> Before {sheep_count}-Sheep ({i}) tries to run away "
                  f"from CW: ({closest_wolf}).")
            i.y = i.y + (i.y - int((i.y + closest_wolf.y)/2))
            i.x = i.x + (i.x - int((i.x + closest_wolf.x)/2))
            i.boundary_conditons() # Check boundary conditions!
            print(f"--> After {sheep_count}-Sheep ({i}) tried to run away "
                  f"from CW ({closest_wolf}).")
            print(f"___________ {sheep_count}-Sheep tried to run away "
                  f"from CW ___________ ")  
   
        # If no CW found:        
        elif closest_wolf == None:
            print(f"-> NO CW FOUND. {sheep_count}-Sheep will try to either, "
                  f"(if energy allows: find CS to move closer+eat "
                  f"OR breed/share) "
                  f"OR (move/eat normally if NO CS or low energy).")
            # min_dist = proximity*0.5 # most prob not needed. will see later. #############
            breed = False # To check if the sheep bred successfully.
            fail_breed = False # To check if breeding failed.
            share = False # To check if resources were shared.
            closest_sheep = None # To target and track the closest sheep (CS)
            sheep2_count = -1 # To assign index to the other sheep.
            min_energy = 600 # Set minimum energy value.
            
            # if store > min_energy, it tries to find CS:
            if i.store > min_energy:
                print(f"->{sheep_count}-Sheep has Store > Min_ernergy"
                      f"({min_energy}) ({i}).")
                # Try to find CS. Slice used as breeding may take place.
                # sheep_index is used as the start index to prevent
                # comparison between same sheep/same pair.
                for j in sheep[sheep_index:]:
                    #Increase the sheep2_count by 1 to assign the j sheep 
                    # it's index value.
                    sheep2_count += 1
                    # Print below tests if looping with i+1 sheep!
                    # eg., if current sheep is no-6, and there are total 
                    # 7 sheep in current iterations, it should loop with 
                    # only 1 sheep. If it's the 7th sheep it loops with none.
                    print(f"--> {sheep_count}-Sheep looping with "
                          f"{sheep2_count}-Sheep.")              
                    
                    # Calculate the distance between itself and other sheep.
                    distance = af.Animal.dist_animals(i, j)
                    
                    # If other sheep is within minimum distance but beyond 
                    # action distance, track it.
                    if action_dist < distance < min_dist:
                        print('---->  (AD < D < MD).')
                        min_dist = distance # Assign the new min_dist.
                        closest_sheep = j # Assign the new CS.
                        print(f"----> Min distance={min_dist} for "
                              f"{sheep_count}-Sheep ({i}) with "
                              f"{sheep2_count}-Sheep ({j}).")  
                    
                    # If other sheep is within actions distance: ACTION!
                    elif distance <= action_dist:
                        # Chance of breeding/fail breeding
                        breeding_chance = 0.50 ############################
                        print(f"----> D <=AD. Sheep Breeding/Sharing "
                              f"proximity of {distance}(<={action_dist}) "
                              f"entered by CS {sheep_count}-Sheep ({i}) with "
                              f"CS {sheep2_count}-Sheep ({j}).")
                        
                        # CS also must have store > min_energy to have a 
                        # chance of breeding.
                        # Sincec CS also has store > min_energy, try breeding.
                        if j.store > min_energy: 
                            print(f"----->{sheep_count}-Sheep ({i}) and CS "
                                  f"{sheep2_count}-Sheep ({j} have "
                                  f"> Min_energy ({min_energy}) store. "
                                  f"So they will try breeding if "
                                  f"p > {breeding_chance}")
                            # Breeding (successful/failed) costs energy and
                            # the new store value of both sheep will be the
                            # half of average of both sheep. This is same
                            # for wolves.
                            breeding_cost = ((i.store + j.store)/2)/2 ###############
                            
                            # if p>breeding_chance, breeds successfully.
                            if random.random() > breeding_chance:
                                print(f"------>1.A. Random>{breeding_chance}."
                                      f" So the sheep will breed.")
                                print(f"------> {sheep_count}-Sheep ({i}) "
                                      f"before breeding with CS "
                                      f"{sheep2_count}-Sheep ({j}).")
                                # Set new store values
                                i.store = breeding_cost
                                j.store = breeding_cost
                                # Append new sheep with +10 y,x of i sheep,
                                # so that it is placed closer when appended.
                                sheep.append(af.Sheep(animals, wolves, sheep,\
                                environment, y=(i.y+10), x=(i.x+10))) ############### This needs checking!
                                # i.boundary_conditons() ############### Not needed here
                                breed = True # Set breed as true.
                                print(f"------> Sheep Breed = {breed}")
                                print(f"------> {sheep_count}-Sheep ({i}) "
                                      f"after breeding with CS "
                                      f"{sheep2_count}-Sheep ({j}).")
                                print(f"_____________ {sheep_count}-Sheep "
                                      f"Mated SUCCESSFULLY with "
                                      f"CS {sheep2_count}-Sheep ____________")
                                # Break away from the loop and go to if 
                                # statement below to move onto next sheep.
                                break
                            
                            # if p<breeding_chance, breeding fails.
                            else:
                                print(f"------>1.B Random <{breeding_chance}."
                                      f" So the breeding will fail.")
                                print(f"------> {sheep_count}-Sheep ({i}) "
                                      f"before failed breeding with "
                                      f"CS {sheep2_count}-Sheep ({j})")
                                # Breeding attempted. Just was not successful!
                                # So energy deduction will be same as 
                                # successful breeding.
                                i.store = breeding_cost 
                                j.store = breeding_cost
                                fail_breed = True # Set fail_breed as true.
                                print(f"------> Failed Sheep Breeding = "
                                      f"{fail_breed}")
                                print(f"------> {sheep_count}-Sheep ({i}) "
                                      f"after failed breeding with "
                                      f"CS {sheep2_count}-Sheep ({j}).")
                                print(f"_____________ {sheep_count}-Sheep "
                                      f"Fail Mated with "
                                      f"CS {sheep2_count}-Sheep ____________")
                                # Break away from the loop and go to if 
                                # statement below to move onto next sheep.
                                break
                        
                        # CS also must have store > min_energy to have a 
                        # chance of breeding.
                        # Since CS does not have >min_energy,
                        # Sheep i and CS j will share store to become average.
                        # They won't fight unlike wolves, as their main
                        # goal is survival.
                        else:
                            print(f"-----> {sheep_count}-Sheep ({i}) and "
                                  f"CS {sheep2_count}-Sheep ({j} will not "
                                  f"mate as CS {sheep2_count}-Sheep store "
                                  f"<{min_energy}. They will share resource "
                                  f"to become average.")
                            # Calculate average store value and assign
                            average = (i.store + j.store)/2 ##########################@@
                            i.store = average
                            j.store = average
                            share = True # Set share as true.
                            print(f"-----> Shared resources = {share}")
                            print(f"-----> {sheep_count}-Sheep ({i}) and "
                                  f"CS {sheep2_count}-Sheep ({j}) "
                                  f"after sharing resources!")
                            print(f"_____________ {sheep_count}-Sheep and "
                                  f"CS {sheep2_count}-Sheep shared "
                                  f"resources ____________")
                            # Break away from the loop and go to if 
                            # statement below to move onto next sheep.
                            break
                
                # when ACTION done, continue to next sheep!
                if breed or fail_breed or share == True:  
                    print(f"_______ Breeding={breed}, "
                          f"Failed breeding={fail_breed}, "
                          f"Share={share} for {sheep_count}-Sheep __________")
                    continue # Continue to next sheep.
                
                # If no sheep within action distance but CS found within
                # minimum distance, track and get closer to it while eating. 
                # This allows to get within action distance and at the same 
                # time, allows the sheep to stay closer like in a herd!
                elif closest_sheep != None:
                    print("->CS Found!")
                    print(f"-> {sheep_count}-Sheep ({i}) before moving "
                          f"closer (while eating) to "
                          f"CS-Sheep: ({closest_sheep}).")
                    # This moving algoright may be improved!
                    i.y = (int((i.y + closest_sheep.y)/2))
                    i.x = (int((i.x + closest_sheep.x)/2))
                    i.boundary_conditons() # Check boundary conditions.
                    i.eat() # Eat while moving like in a herd!
                    print(f"-> {sheep_count}-Wolf ({i}) after moving closer "
                          f"(while eating) to CS-Sheep: ({closest_sheep}).")
                    print(f"___________ {sheep_count}-Sheep moved "
                          f"closer CS___________" )                   
                
                # If No CS found, but has store>min_energy, moves and eats.
                else:
                    print("-> NO CS Found.")
                    print(f"-> {sheep_count}-Sheep ({i}) before normally "
                          f"moving and eating.")
                    i.move()
                    i.eat()
                    print(f"-> {sheep_count}-Sheep ({i}) after normally "
                          f"moving and eating.")
                    print(f"...e1________ {sheep_count}-Sheep moved "
                          f"normally and ate ___________")
            
            # If store < min_energy, move and eat
            else:
                print(f"->{sheep_count}-Sheep has Store < "
                      f"Min_ernergy({min_energy}) ({i}). "
                      f"So moves and eat")
                print(f"-->{sheep_count}-Sheep ({i}) before normal moving "
                      f"and eating")
                i.move()
                i.eat()
                print(f"-->{sheep_count}-Sheep ({i}) after normal moving "
                      f"and eating")
                print(f"___e2________ {sheep_count}-Sheep moved normally "
                      f"and ate ___________")
        
        # Add a space between two sheep printouts
        print('')        
    print('________________Sheep Cycle Ends_________________')
    print('________________Wolf Cycle Begins________________')
       
    wolf_count = -1 # To assign the current wolf it's index value.
    # wolf_index used to prevent comparison between same wolf/pair, 
    # used in j wolf slice as stratin index.
    wolf_index = 0 
    for i in wolves[:]:
        wolf_count += 1 # Assign the current wolf it's index value.
        wolf_index += 1 # Increase by 1 to prevent comparsion between same w/p.
        min_energy = 500 # Set min_energy for breeding?????
        bf_e = 0.5 # Set probability value
        # The if conditon below: If wolf has > twice the minimum energy,
        # its vision improves, meaning its proximity is doubled.
        if i.store > min_energy*2:
            min_dist = proximity*2
        else:
            min_dist = proximity
        print('') # Add space between two wolves printouts.
        print(f"---------{wolf_count}-Wolf initialised with ({i}) --------")
        
        # Actions for the current wolf:
        # 1. If (current wolf store <=min_energy) OR (store>min_energy AND  
        # p between bf_e/2 and <bf_e (which if bf_e not changed means,  
        # p is between 0.25 and <0.50)), then try find closest sheep (CS) to 
        # move closer to or if within action distance then eat. If no CS 
        # found, then just move randomly.
        # 2. Else if the (current wolf store >min_energy AND p >= bf_e)  
        # (i.e., 0.5 if unchanged), it tries to find closest_wolf (CW) to move
        # closer to, or if within action distance: breeds or fights. If no
        # CW found, moves randomly.
        # 3. Else if (current wolf store >min_energy AND p<bf_e/2) (i.e., 
        # <0.25 if bf_e unchanged, the current wolf moves randomly.) 
        
        
        # 1. If (current wolf store <=min_energy) OR (store>min_energy AND  
        # p between bf_e/2 and <bf_e (which if bf_e not changed means,  
        # p is between 0.25 and <0.50)), then try find closest sheep (CS) to 
        # move closer to or if within action distance then eat. If no CS 
        # found, then just move randomly.
        # #Check if (current wolf store <=min_energy) OR (store>min_energy AND  
        # #p between bf_e/2 and <bf_e)
        if i.store <= min_energy or (i.store > min_energy and\
           ((bf_e/2) <= random.random() < bf_e)): ######################################
            if i.store <= min_energy:
                print(f"--> {wolf_count}-Wolf has <=Min_energy({min_energy}) "
                      f"store ({i}). Tries to find food (sheep).")
            else:
                print(f"--> {wolf_count}-Wolf has >Min_energy({min_energy}) "
                      f"store ({i}) and {bf_e/2} <= random.random() < {bf_e}."
                      f" Tries to find food (sheep).")
            
            sheep_count = -1 # To assign sheep its index value.
            closest_sheep = None # To assign and track closest sheep (CS)
            eaten = False # Set eat as false.
            
            # Loop through sheep list to find CS.
            # Slice is used for sheep list as sheep might get eaten by wolf.
            # No starting index is used in slice as each wolf should go 
            # through each sheep.
            for j in sheep[:]:
                sheep_count += 1 # Assign sheep its index value.
                print(f"---> {wolf_count}-Wolf looping with "
                      f"{sheep_count}-Sheep")              
                
                # Check distance between current wolf and sheep
                distance = af.Animal.dist_animals(i, j)
                # print(f"distance={distance} between {i}-Wolf ({wolves[i]}) "
                #      f"and {sheep_count}-Sheep ({j})")

                # If wolf find a CS within action distance: eats it!
                if distance <= action_dist:
                    # Eats the first CS sheep at action distance. 
                    # So should not loop through the other ones.
                    print(f"----> CS within {distance} which is "
                          f"<= action distance ({action_dist}).")
                    print(f"----> {wolf_count}-Wolf ({i}) before eating "
                          f"CS {sheep_count}-Sheep ({j})")
                    # Wolf eats 4/5 of the sheep as can't eat everything!
                    # The rest of the 1/5 is returned to the environment.
                    i.store += (j.store*(4/5)) # Wolf eats 4/5
                    env_rcv = (j.store*(1/5)) # Environment received 1/5
                    i.environment[i.y][i.x] += env_rcv 
                    j.store = 0 # CS store is 0
                    print(f"---->Env received ({env_rcv}).")
                    print(f"----> {wolf_count}-Wolf ({i}) after eating "
                          f"CS {sheep_count}-Sheep ({j}).")
                          # f"Env received ({env_rcv})")
                    sheep.remove(j)
                    eaten = True # Set eat as true
                    # Eaten, so break (don't eat other CS within AD and 
                    # go to if below (and continue)
                    break 
                # If CS within min_dist but beyond action distance, assign
                # CS with closest_sheep and track it (move closer)
                elif action_dist < distance < min_dist:
                    print(f"----> action_dist({action_dist}) < "
                          f"distance({distance}) < min_dist({min_dist}).")
                    # Set new minimum distance & 
                    # update if even closer sheep found
                    min_dist = distance 
                    # Set new CS & update if closer sheep found
                    closest_sheep = j 
                    print(f"----> Min Distance = {min_dist} for "
                          f"{wolf_count}-Wolf ({i}) with "
                          f"{sheep_count}-Sheep ({j}).")
            
            # Comes here from the break above if eaten = True.
            # Continue to next sheep.
            if eaten == True:
                print(f"___________ Eaten={eaten}. {wolf_count}-Wolf ate "
                      f"CS {sheep_count}-Sheep__________")
                continue # Move on to next wolf.   
            
            # if CS found (but beyond action distance) within minimum
            # distance, chase it!
            elif closest_sheep != None:
                print(f"-> CS Found!")
                print(f"--> {wolf_count}-Wolf ({i}) before moving closer to "
                      f"CS ({closest_sheep }).")
                # The below move algorithm should be improved!
                # Here no energy is lost while chasing. So can add some
                # energy loss.
                i.y = (int((i.y + closest_sheep.y)/2))
                i.x = (int((i.x + closest_sheep.x)/2))
                i.boundary_conditons() # Check boundary conditions.
                print(f"--> {wolf_count}-Wolf ({i}) after moving closer to "
                      f"CS ({closest_sheep }).")
                print(f"___________ {wolf_count}-Wolf moved closer "
                      f"to CS___________")           
            
            # If no CS found, wolf moves randomly based on move() method.
            else: 
                print(f"-> No CS found!")
                print(f"-->else1 begins: {wolf_count}-Wolf ({i}) "
                      f"before normal moving")
                i.move()
                print(f"-->else1 ends: {wolf_count}-Wolf ({i}) "
                      f"after normal moving")
                print(f"....el1___________ {wolf_count}-Wolf moved "
                      f"normally___________") #el1 - for debugging purpose.
        
        #2. Else if the (current wolf store >min_energy AND p >= bf_e)  
        # (i.e., 0.5 if unchanged), it tries to find closest_wolf (CW) to move
        # closer to, or if within action distance: breeds or fights. If no
        # CW found, moves randomly.        
        elif i.store > min_energy and random.random() >= bf_e: 
            print(f"--> {wolf_count}-Wolf has > {min_energy} store ({i}) "
                  f"and Random >= {bf_e}. so will try to find CW to move "
                  f"closer or breed/fight if within AD({action_dist}).")
            fight = False # Set fight as false. will turn True if fought.
            breed = False # Will turn true if bred successfully.
            fail_breed = False # Will turn true if failed breeding.
            closest_wolf = None # To assign and track closest_wolf
            wolf2_count = -1 # To assign and track other wolves.
            
            # Slice is used as wolves might breed new wolves.
            # wolf_index is used as the starting index so that action is 
            # not duplicated for same wolf or same pair.
            for j in wolves[wolf_index:]:
                wolf2_count += 1 # Assign the other wolf it's index.
                print(f"---> {wolf_count}-Wolf looping with "
                      f"{wolf2_count}-Wolf")
                
                # Check distance between wolves
                distance =  af.Animal.dist_animals(i, j)
                
                # If a wolf between min_dist but beyond action_distance
                # assign it as the closest wolf and update minimum distance
                if action_dist < distance < min_dist: 
                    print('----> (AD2 < D < MD).')
                    min_dist = distance # Assign (and update if closer found)
                    closest_wolf = j # Assign (and update if closer found)
                    print(f"----> Min distance={min_dist} for "
                          f"{wolf_count}-Wolf ({i}) with "
                          f"{wolf2_count}-Wolf ({j})")  
                
                # If a wolf is within action distance: ACTION    
                elif distance <= action_dist:
                    print(f"----> d<=ad. breeding/fight roximity of "
                          f"{distance}(<={action_dist}) entered by "
                          f"{wolf_count}-Wolf ({i}) with CW "
                          f"{wolf2_count}-Wolf ({j}).")
                    
                    # If CW has > min store value (min_energy), breed 
                    # successful if p is > bf_e (0.50 if unchanged). If 
                    # p <= bf_e the wolves will try to breed but will fail.
                    if j.store > min_energy:
                        print(f"-----> CW {wolf2_count}-Wolf ({j} has > "
                              f"{min_energy} store. So they will try "
                              f"breeding. {bf_e*100}% probability of "
                              f"breeding successfully.")
                        
                        # Breeding (successful/failed) costs energy and
                        # the new store value of both wolves will be the
                        # half of average of both wolves. This is same for 
                        # sheep breeding.
                        breeding_cost = ((i.store + j.store)/2)/2 ######################
                        if random.random() > bf_e:
                            print(f"------>1.A. Random >{bf_e}. "
                                  f"So the wolves will mate.")
                            print(f"------> {wolf_count}-Wolf ({i}) before "
                                  f"mating with CW {wolf2_count}-Wolf ({j})")
                            i.store = breeding_cost
                            j.store = breeding_cost
                            wolves.append(af.Wolf(animals, wolves, sheep,\
                                         environment, y=(i.y+5), x=(i.x+5)))#####################
                            breed = True # Set breed as true!
                            print(f"------> Breed = {breed}")
                            print(f"------> {wolf_count}-Wolf ({i}) after "
                                  f"mating with CW {wolf2_count}-Wolf ({j})")
                            print(f"_____________ {wolf_count}-Wolf Mated "
                                  f"SUCCESSFULLY with "
                                  f"CW {wolf2_count}-Wolf ____________")
                        else: # p <= bf_e
                            print(f"----->1.B. Random <{bf_e}. "
                                  f"So breeding will not be successful.")
                            print(f"----->{wolf_count}-Wolf ({i}) before "
                                  f"fail breeding with "
                                  f"CW {wolf2_count}-Wolf ({j})")
                            i.store = breeding_cost
                            j.store = breeding_cost  
                            fail_breed = True # Set fail_breed as True
                            print(f"------> Fail Breeding = {fail_breed}")
                            print(f"_____________ {wolf_count}-Wolf ({i}) "
                                  f"after FAILED BREEDING with "
                                  f"CW {wolf2_count}-Wolf ({j})")
                        
                        # Current wolf attempted breeding (successfully or 
                        # unsuccessfully) with the first CW. So should not 
                        # try with other CW even if within action distance.
                        # So break and go below to if and continue to next
                        # wolf.
                        break
                    
                    # If CW is within action distance but energy < minimum 
                    # energy, then the wolves will fight! The winner depends
                    # on probability. If p > bf_e current wolf will win 
                    # bf_e*store of the CW and vice versa if p <= bf_e.
                    # So if bf_e unchanged, p is 0.50. So if p>0.50, current 
                    # wolf will 0.5*store of CW, which is half the store.
                    else:
                        print(f"----->2.A. CW {wolf2_count}-Wolf has "
                              f"< than {min_energy} store")
                        print(f"------>{wolf_count}-Wolf ({i}) will FIGHT "
                              f"CW {wolf2_count}-Wolf ({j}) & move") 
                        
                        if random.random() > bf_e:
                            print(f"------>2.A.i. Random > {bf_e}. So "
                                  f"{wolf_count}-Wolf will win {bf_e*100}% "
                                  f"of CW {wolf2_count}-Wolf store.")
                            # This is what current wolf i will gain and CW j
                            # will loose. See above description.
                            gain = (j.store*bf_e) 
                            i.store += gain
                            j.store -= gain
                            # The current wolf will also move after fighting
                            # based on move method.
                            i.move()
                            print(f"------> {wolf_count}-Wolf ({i}) won+moved"
                                  f" after fighting with "
                                  f"CW {wolf2_count}-Wolf ({j})")
                        
                        # if p<= bf_e
                        else: 
                            print(f"------>2.A.ii. Random < {bf_e}. So "
                                  f"{wolf_count}-Wolf will loose {bf_e*100}% "
                                  f"store to CW {wolf2_count}-Wolf")
                            # This is what current wolf i will lose and CW j
                            # will gain. See above description.
                            lose = (i.store*bf_e)
                            i.store -= lose
                            j.store += lose
                            # The current wolf will also move after fighting
                            # based on move method.
                            i.move()
                            print(f"------> {wolf_count}-Wolf ({i}) lost+moved"
                                  f" after fighting with CW "
                                  f"{wolf2_count}-Wolf ({j})")
                            
                        # Set fight as true for current wolf!    
                        fight = True 
                        print(f"------> Fight = {fight}")
                        print(f"_____________ {wolf_count}-Wolf Fought-(2) "
                              f"with CW {wolf2_count}-Wolf ____________")
                        # Current wolf already interacted with CW within
                        # action distance. So break and go to below if 
                        # and continue to next wolf!
                        break
                    
            # If current wolf interacted with CW within action distance,
            # continue to the next wolf.
            if breed or fail_breed or fight == True:   
                print(f"_______ Breed={breed}, Failed Breed={fail_breed}, "
                      f"Fought={fight} for {wolf_count}-Wolf __________")
                continue
            
            # If CW found within min_distance but beyond action distance,
            # get close to it.
            elif closest_wolf != None:
                print("->CW Found!")
                print(f"-> {wolf_count}-Wolf ({i}) before moving closer to "
                      f"CW-Wolf: ({closest_wolf}).")
                # This move algorithm should be improved!
                i.y = (int((i.y + closest_wolf.y)/2))
                i.x = (int((i.x + closest_wolf.x)/2))
                i.boundary_conditons() # Check boundary conditons.
                print(f"-> {wolf_count}-Wolf ({i}) after moving closer to "
                      f"CW-Wolf: ({closest_wolf}).")
                print(f"_______ {wolf_count}-Wolf moved closer CW+_______") 
                
            # If No CW found, move as per the move method.
            else: # No CW. E>min_energy and p>bf_e
                print(f"-> No CW found. although store >{min_energy} and "
                      f"p>={bf_e}!")
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) before "
                      f"normal moving.")
                i.move()
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) after "
                      f"normal moving.")
                print(f".... el2 _______  {wolf_count}-Wolf "
                      f"moved normally _______ ")
        
        # If if and elif not satisfied, just move based on move method.
        else:
            # This area may also be made as as a rest area for wolves
            # based on probability.
            print("--> if and elif not satisfied")
            print(f"--> {wolf_count}-Wolf has > Min_energy({min_energy}) "
                  f"store ({i}) but Random < bf_e/2({bf_e/2}). "
                  "So will move normally.")
            print(f"--->else3 begins: {wolf_count}-Wolf ({i}) before "
                  f"normal moving.")
            i.move()
            print(f"--->else3 begins: {wolf_count}-Wolf ({i}) after "
                  f"normal moving.")
            print(f"....e3_______ {wolf_count}-Wolf moved normally_______")
    print('________________Wolf Cycle Ends_________________')
    
    # Display environment, wolves and sheep!    
    plt.ylim(0, len(environment))
    plt.xlim(0, len(environment[0])) 
    plt.imshow(environment)
    # sheep, not no_sheep is used as the initial number of sheep may be
    # altered via breeding or being eated by wolves. Same for wolves, as wolves
    # might breed new wolves. Note, wovles do not die!
    for i in range(len(sheep)):
        # If the color is removed, sheep and wolves will have different
        # colours at each iteration as their initialisation will be 
        # randomly determined by random shuffle. 
        plt.scatter(sheep[i].x, sheep[i].y, marker="p", color='white')
    for j in range(len(wolves)):
        plt.scatter(wolves[j].x, wolves[j].y, marker="v", color='black')

# Set up generator
def gen_function(b = no_iterations):
    a = 0
    while a < b:
        yield a
        a += 1
        
# Set up run function for use with tkinter GUI
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update,\
                frames=gen_function, interval=100, repeat=False, save_count=no_iterations)
    # Save animation not working. ffmepg not found! had to install!
    # Writer = matplotlib.animation.writers['ffmpeg']
    # writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
    # animation.save('ABM.mp4', writer=writer)
    # writergif = matplotlib.animation.PillowWriter(fps=60) 
    # animation.save('ABM.gif', writer=writergif)
    
    # .show() is deprecated.
    canvas.draw()
  
# Set up GUI
root = tkinter.Tk()
root.wm_iconbitmap('logo.ico')
root.wm_title("Sheep and Wolves - Agent Based Model (ABM) by Mushtahid!")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Menu", menu=model_menu)
model_menu.add_command(label="Run ABM Model", command=run)
tkinter.mainloop()

# Close the prinout to log file!
sys.stdout.close()
sys.stdout=stdoutOrigin
