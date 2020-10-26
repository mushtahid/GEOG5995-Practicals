# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 09:26:33 2020

@author: Md Mushtahid Salam
email: mushtahid@gmail.com
"""
# Import modules
# import sys # To print the output in a seperate text file
import TESTAF1 as af # Import the agentframework
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
import time # To time the process time for each iteration and total model


# Print out the output in a text file. Better for debuggin the code as it 
    # can be searched easily using printed texts/keywords using NotePad++ or 
    # other similar text editors!
# WARNING:
# Recommended to enable the stdout code if you want to debug! Make sure to
    # uncomment sys module and also look at the end of the code to uncomment
    # closing stdout.
# Otherwise if the file is run from, it will not display any prompts to run 
    # the code! However, if the code is run from Spyder it will work 
    # with stdout.
# See the end as well for closing the stdout. 
# stdoutOrigin = sys.stdout
# sys.stdout = open("log.txt", "w")

# Scrape web data to find x and y values for the sheep!
r = requests.get('http://bit.ly/GeogLeedsAFData')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
# print(td_ys)
# print(td_xs)

# Set up plot size and axes
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
# ax.set_autoscale_on(False) 

# Modifiable variables!
# Prompt if want to modify:
modify = input("- Do you want to change the modifiable variable? Enter "\
               "'y' (lowercase) if YES. You can still choose to run with "\
               "default values for individual variables if you chosse yes. "\
               "If NO, enter any other value to run the model "\
               "with default values: ")
correct_y = "y"
if modify == correct_y:    
    # Number of sheep
    n_sh = input('- Enter number of sheep. (Or press enter to use default'\
                 ' value 15): ')
    try:
        no_sheep = int(n_sh)
    except:
        no_sheep = 15
        print('Invalid characters/No number entered! Model will run with '\
              '15 sheep.')
    # Number of wovles 
    n_wl = input('- Enter number of wolves. (Or press enter to use default '\
                 'value 5): ')
    try:
        no_wolves = int(n_wl)
    except:
        no_wolves = 5
        print('Invalid characters/No number entered! Model will run with '\
              '5 wolves.')    
    # Input number of iterations
    n_it = input('- Enter number of iterations. (Or press enter to use '\
                 'default value 100): ')
    try:
        no_iterations = int(n_it)
    except:
        no_iterations = 100 # Number of times the animation will run
        print('Invalid characters/No number entered! Model will run with '\
              'default of 100 iterations.')     
    # Input proximity
    prox = input('- Enter proximity value. Proximity refers to the range of '\
                 'vision or distance within which WOLVES can observe and '\
                 'notice other animals and determine the closest one. '\
                 '(Or press enter to use default value 50): ')
    try:
        proximity = int(prox)
    except:
        proximity = 50 # the range of vision of the wolves
        print('Invalid characters/No number entered! Model will run with '\
              'default of wolf proximity of 50.')        
    # Input the denometer for sheep minimum distance.
    smd = input('- Enter the sheep proximity denominator. By default, the '\
                'proximity of sheep is half of that of wolves. '\
                'i.e, proxmity/2. This is because sheep is a prey! '\
                'You can change the denominator to alter the '\
                'sheep proximity. (Or press enter to use default '\
                'denominator value 2): ')
    try:
        smd_denometer = int(smd)
    except:
        smd_denometer = 2
        print('Invalid characters/No number entered! Model will run with '\
              'default sheep proximity denominator of 2.')        
    # Input action_dist
    actd = input('- Enter the action distance within which the animals will '\
                 'interact, such as breed, fight and so on. Same for sheep '\
                 'and wolves. (Or press enter to use default value 5): ')
    try:
        action_dist = int(actd)
    except:
        action_dist = 5 # Proximity within which animals can interact,eg breed.
        print('Invalid characters/No number entered! Model will run with '\
              'default action distance of 5.') 
    # Input probability
    prob = input('- Enter sheep breeding probability. Probability represents '\
                 'the chance of breeding for sheep, e.g., '\
                 'if the probability>0.5, the sheep will breed '\
                 'successfully, i.e., if random value>0.5. Otherwise '\
                 'breeding attempt will fail. Note: for breeding to be '\
                 'successfull, randome value hasto be MORE than the '\
                 'probability value (random value>probability). '\
                 'You can change it. (Or press enter to use default '\
                 'value 0.5): ')
    try:
        probability = float(prob) # Need conditions to make it between 0 - 1.
    except:
        probability = 0.50 
        print('Invalid characters/No number entered! Model will run with '\
              'default sheep probability value of 0.5.')
    # Input probability for wolves
    wolf_prob = input("- The probability of breeding for wolves by default "\
                 f"is the same as that of sheep probability: {probability}. "\
                 "For wolves, this also represents the chance of winning a "\
                 "fight with other wolves. It also determines fraction of "\
                 "the losing wolf's store the winning wolf will win. "\
                 "You can change it. Note: for breeding/fight "\
                 "to be successfull, random value has to be MORE than "\
                 "the probability value (i.e., random>probability). "\
                 "You can chagne it. (Or press enter to use sheep "\
                 f"probability value ({probability}): ")
    try:
        bf_e = float(wolf_prob) # Need conditions to make it between 0 - 1.
    except:
        bf_e = probability
        print('Invalid characters/No number entered! Model will run with '\
              'default wolf probability that is the same as sheep '\
              f'probability: {probability}.')       
    # Input the sheep minimum energy
    sme = input("- Sheep need a minimum energy/store to breed. "\
                 "You can change it. (Or press enter to use default store "\
                 "value 600): ")
    try:
        s_min_energy = int(sme)
    except:
        s_min_energy = 600 # Set minimum energy value for sheep to breed.
        print('Invalid characters/No number entered! Model will run with '\
              'default sheep minimum energy/store needed for action of 600.')
    # Input the wolf minimum energy
    wme = input("- Wolves also need a minimum energy/store to breed. "\
                 "You can change it. (Or press enter to use default store "\
                 "value 500): ")
    try:
        min_energy = int(wme)
    except:
        min_energy = 500 # Set wolves minimum store value for breeding.
        print('Invalid characters/No number entered! Model will run with '\
              'default wolf minimum energy/store needed for action of 500.')
    # Input the wolf high store multiplier
    hstm = input("- Wolves have the extra ability to increase their "\
                 "proximity once they have a store value above a "\
                 "certain threshold. "\
                 "For example, the default is double that of minimum "\
                 "energy, i.e., if store>min_energy*2, then proximity "\
                 "will also be doubled!. You can change this Multiplier. "\
                 "(Or press enter to run with default multiplier of 2): ")
    try:
        high_store_mp = int(hstm)
    except:
        # Hight store multiplier: to increase the proximity of wolves if they 
        # have a certain amount energy more than the minimum energy
        high_store_mp = 2
        print('Invalid characters/No number entered! Model will run with '\
              'default multiplier value of 2.')
else:
    
    no_sheep = 15
    no_wolves = 5
    no_iterations = 100 
    proximity = 50
    smd_denometer = 2
    action_dist = 5 
    probability = 0.50
    bf_e = probability
    s_min_energy = 600 
    min_energy = 500
    high_store_mp = 2
    print('____Model will run with default variables____')
    print(f"Number of sheep: {no_sheep}")
    print(f"Number of wolves: {no_wolves}")
    print(f"Number of iterations: {no_iterations}")
    print(f"Wolf proximity: {proximity}")
    print(f"Sheep proximity denominator: {smd_denometer} and so sheep "\
          f"proximity: {proximity/smd_denometer}")
    print(f"Action distance: {action_dist}")
    print(f"Sheep probability: {probability}")
    print(f"Wolf probability: {bf_e}")
    print(f"Sheep minimum energy: {s_min_energy}")
    print(f"Wolf minimum energy: {min_energy}")
    print(f"Wolf high store multiplier: {high_store_mp}")
    print('') # Add blank space

# Variables that should not be altered.
environment = []
sheep = []
wolves = []
total_time = 0 # Set initial total process time as zero.
sheep_min_dist = proximity/smd_denometer # Sheep minimum distance
total_sheep_store = 0.0 # For calculating the toal sheep store as float.
t_sheep_store_list = [] # For use in writing the total sheep store in a file.
total_wolves_store = 0.0 # For calculating the toal wovles store as float.
t_wolves_store_list = [] # For use in writing the total wolves store in a file.
it_no = -1 # No counting the number of iterations.

# no_sheep = 15
# no_wolves = 5
# proximity = 50 # the range of vision of the animals
# no_iterations = 100 # Number of times the animation will run
# action_dist = 5 # Proximity within which animals can interact, eg breed etc.
# probability = 0.50 
# s_min_energy is the minimum required energy/store for sheep to perform
# an action (e.g. breed) if CS is within actions distance of 5.
# s_min_energy = 600 # Set minimum energy value for sheep to breed.
# Wolf variables
# min_energy = 500 # Set wolves minimum store value for breeding.
# bf_e = probability # Can be altered to change probability value for wolves!
# high_store_mp = 2

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
# Multiply x and y with 3 to make them more spread out. However, I did not
# as the sheep should stay in a herd. So makes sense for them to appear 
# closer within a grid of 100X100 as assigned by the webdata!
    y = int(td_ys[i].text) 
    x = int(td_xs[i].text)
    sheep.append(af.Sheep(wolves, sheep, environment, y, x)) 
# print('Initial number of  sheep: ', len(sheep))

# Initialise wolves
for i in range(no_wolves):
    y = None #int(td_ys[-i].text)*3 #interesting!
    x = None #int(td_xs[-i].text)*3
    wolves.append(af.Wolf(wolves, sheep, environment, y, x))
# print('Initial number of  wolves:', len(wolves))
       
# Set up update/frames for animation
def update(frame_number):
    """Updates the animation frame with the new parameters"""

    # Start the timer
    start = time.process_time()
    # Clear the figure from previous iteration!
    fig.clear()
    # Call global it_no to update it at each iteration.
    global it_no
    it_no += 1
    print('') # Add a space between two printouts!
    print(f"*************** ITERATION NUMBER {it_no} BEGINS ************")
    
    # Randomly shuffle the order of initialisation for the animals
    # at each iteration so that everyone gets a fair shot at 
    # whatever their action is (eating/breeding/mating/fighting etc.)
    # Comment out the random.shuffle for debugging.
    random.shuffle(sheep)
    random.shuffle(wolves)
    
    # S.1
    # sheep_count tracks the current sheep (i) via it's index value.
    sheep_count = -1
    # sheep_index tracks the other sheep (j) with which  the current sheep 
    # interacts with via their index value. Used to prevent the current sheep 
    # from interacting with itself and prevent interaction of the same pair
    # in the same iteration.
    sheep_index = 0
    # slice [:] is used in for loop because sheep may breed 
    # with each other.
    for i in sheep[:]:
        sheep_count += 1 # Increase by 1 to assign the i sheep it's index.
        sheep_index += 1 # Increase by 1 to use as the start index 
                         # when comapring with other sheep.
        
        # s_min_dist (minimum distance) for sheep is sheep_min_dist, which is
        # half of proximity as sheep is a prey! Wolves have higer field of 
        # vision, so they have access to full proximity distance!
        s_min_dist = sheep_min_dist
        
        # closest_wolf targets and tracks the closest wolf to run away from!
        closest_wolf = None
        # print(sheep_count)
        # print(sheep_index)
        # print(s_min_dist)
        # print(closest_wolf)
        
        print('') # Add blank space
        print(f"-> ----- {sheep_count}-Sheep initialised with ({i}) ------")

        # Actions for sheep: check for close wolves (CW) within s_min_dist. 
        # If found, run away. While running away it does not eat.
        # If no CW. Looks for close sheep (CS) if it has s_min_energy to move 
        # closer/breed/share. While moving closer it eats as well. If no CS
        # found but has s_min_energyit moves randomly and eats. If it does not 
        # have s_min_energy then it moves randomly and eats.
        
        # S.1.1
        # For j loop below, range(len(wolves)) is used. Slice of wolves 
        # is not used for looping with sheep as the wolves will not mate with 
        # sheep to increase the number of wolves. range(no_wolves) is not used
        # as no_wolves represents inital wolf number and the wolves may breed
        # (see further below_ to increase their numbers, and so would fail 
        # the model if used.
        for j in range(len(wolves)):
            # Print below tests if current sheep is looping with all wolves!
            print(f"--> {sheep_count}-Sheep looping with {j}-Wolf.")             
            # Calculate the distance between itself and all wolves.
            # distance = af.Animal.dist_animals(i, wolves[j]) # This works too.
            distance = i.dist_animals(wolves[j])
            # print(f"--> distance={distance} for {i}-Sheep ({sheep[i]}) with"
            #       f"{j}-Wolf ({wolves[j]})")
            
            # S.1.1.1
            # If wolf(ves) detected within s_min_dist, find the 
            # closest wolf (CW).
            if distance < s_min_dist: # d<md+ as keyword for debugging.
                print(f"--->d<md+...{sheep_count}-Sheep noticed "
                      f"closest {j}-Wolf ...") # This may be commented off!
                s_min_dist = distance # Assign the new s_min_dist
                closest_wolf = wolves[j] # Assign the new CW
                print(f"---> {sheep_count}-Sheep ({i}) detected {j}-Wolf "
                      f"({wolves[j]}) within d={s_min_dist}.")            
        # S.1.2
        # If CW found, try to run away!
        if closest_wolf != None:
            # The algorithm may be improved here based on store 
            # and probability
            print("-> CW FOUND.")
            print(f"--> Before {sheep_count}-Sheep ({i}) tries to run away "
                  f"from CW: ({closest_wolf}).")
            # Call the run_from_cw method from Sheep class to run away from CW
            i.run_from_cw(closest_wolf) # Works!
            print(f"--> After {sheep_count}-Sheep ({i}) tried to run away "
                  f"from CW ({closest_wolf}).")
            print(f"___________ {sheep_count}-Sheep tried to run away "
                  f"from CW ___________ ")  
        # S.1.3
        # If no CW found:        
        elif closest_wolf == None:
            print(f"-> NO CW FOUND. {sheep_count}-Sheep will try to either, "
                  f"(if energy allows: find CS to move closer+eat "
                  f"OR breed/share) "
                  f"OR (move/eat normally if NO CS or low energy).")
            breed = False # To check if the sheep bred successfully.
            fail_breed = False # To check if breeding failed.
            share = False # To check if resources were shared.
            closest_sheep = None # To target and track the closest sheep (CS)
            sheep2_count = -1 # To assign index to the other sheep.
            
            # SC.1.3.1
            # if store > s_min_energy, it tries to find CS:
            if i.store > s_min_energy:
                print(f"->{sheep_count}-Sheep has Store > Min_ernergy"
                      f"({s_min_energy}) ({i}).")
                # S.1.3.1.1
                # Try to find CS. Slice used as breeding may take place.
                # sheep_index is used as the start index to prevent
                # comparison between same sheep/same pair.
                for j in sheep[sheep_index:]:
                    # Increase the sheep2_count by 1 to assign the j sheep 
                    # it's index value.
                    sheep2_count += 1
                    # Print below tests if looping with i+1 sheep!
                    # eg., if current sheep is no-6, and there are total 
                    # 7 sheep in current iterations, it should loop with 
                    # only 1 sheep. If it's the 7th sheep it loops with none.
                    print(f"--> {sheep_count}-Sheep looping with "
                          f"{sheep2_count}-Sheep.")              
                    
                    # Calculate the distance between itself and other sheep.
                    # distance = af.Animal.dist_animals(i, j) # This woks too.
                    distance = i.dist_animals(j)
                    
                    # S.1.3.1.1.a
                    # If other sheep is within minimum distance but beyond 
                    # action distance, track it.
                    if action_dist < distance < s_min_dist:
                        print('---->  (AD < D < MD).')
                        s_min_dist = distance # Assign the new s_min_dist.
                        closest_sheep = j # Assign the new CS.
                        print(f"----> Min distance={s_min_dist} for "
                              f"{sheep_count}-Sheep ({i}) with "
                              f"{sheep2_count}-Sheep ({j}).")  
                    
                    # S.1.3.1.1.b
                    # If other sheep is within actions distance: ACTION!
                    elif distance <= action_dist:
                        print(f"----> D <=AD. Sheep Breeding/Sharing "
                              f"proximity of {distance}(<={action_dist}) "
                              f"entered by CS {sheep_count}-Sheep ({i}) with "
                              f"CS {sheep2_count}-Sheep ({j}).")
                        # S.1.3.1.1.b.1
                        # CS also must have store>s_min_energy to have a 
                        # chance of breeding.
                        # Sincec CS also has store>s_min_energy, try breeding.
                        if j.store > s_min_energy: 
                            print(f"----->{sheep_count}-Sheep ({i}) and CS "
                                  f"{sheep2_count}-Sheep ({j} have "
                                  f"> Min_energy ({s_min_energy}) store. "
                                  f"So they will try breeding if "
                                  f"p > {probability}")
                            # Call the breed_cost method from Parent class
                            # to calculate the new store value after breeding
                            # attemp (regardless of successful/failed)
                            breeding_cost = i.breed_cost(j) #This works!
                            
                            # S.1.3.1.1.b.1.1
                            # if p>probability, breeds successfully.
                            if random.random() > probability:
                                print(f"------>1.A. Random>{probability}."
                                      f" So the sheep will breed.")
                                print(f"------> {sheep_count}-Sheep ({i}) "
                                      f"before breeding with CS "
                                      f"{sheep2_count}-Sheep ({j}).")
                                # Set new store values
                                i.store = breeding_cost
                                j.store = breeding_cost
                                
                                # Append new sheep with +10 y,x of i sheep,
                                # so that it is placed closer when appended.
                                sheep.append(af.Sheep(wolves, sheep,\
                                environment, y=(i.y+10), x=(i.x+10)))
                                    
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
                                # This is because the sheep has already 
                                # interacted with a CS. So should not repeat
                                # if another CS present within action_dist.
                                break
                            
                            # S.1.3.1.1.b.1.2
                            # if p<probability, breeding fails.
                            else:
                                print(f"------>1.B Random <{probability}."
                                      f" So the breeding will fail.")
                                print(f"------> {sheep_count}-Sheep ({i}) "
                                      f"before failed breeding with "
                                      f"CS {sheep2_count}-Sheep ({j})")
                                # Breeding attempted. Just was not successful!
                                # So energy deduction will be same as 
                                # successful breeding.
                                i.store = breeding_cost 
                                j.store = breeding_cost
                                
                                # Set fail_breed as true.
                                fail_breed = True
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
                                # This is because the sheep has already 
                                # interacted with a CS. So should not repeat
                                # if another CS present within action_dist.
                                break
                            
                        # S.1.3.1.1.b.2
                        # CS also must have store > s_min_energy to have a 
                        # chance of breeding.
                        # Since CS does not have >s_min_energy,
                        # Sheep i and CS j will share store to become average.
                        # They won't fight unlike wolves, as their main
                        # goal is survival.
                        else:
                            print(f"-----> {sheep_count}-Sheep ({i}) and "
                                  f"CS {sheep2_count}-Sheep ({j} will not "
                                  f"mate as CS {sheep2_count}-Sheep store "
                                  f"<{s_min_energy}. They will share resource"
                                  f" to become average.")
                            # Calculate average store value and assign
                            # The average may be converted into a method
                            # as well.
                            average = (i.store + j.store)/2
                            
                            # Set store values as average
                            i.store = average
                            j.store = average
                            
                            # Set share as true.
                            share = True 
                            print(f"-----> Shared resources = {share}")
                            print(f"-----> {sheep_count}-Sheep ({i}) and "
                                  f"CS {sheep2_count}-Sheep ({j}) "
                                  f"after sharing resources!")
                            print(f"_____________ {sheep_count}-Sheep and "
                                  f"CS {sheep2_count}-Sheep shared "
                                  f"resources ____________")
                            
                            # Break away from the loop and go to if 
                            # statement below to move onto next sheep.
                            # This is because the sheep has already 
                            # interacted with a CS. So should not repeat
                            # if another CS present within action_dist.
                            break
                
                # S.1.3.1.2
                # when ACTION done, continue to next sheep!
                if breed or fail_breed or share == True:  
                    print(f"_______ Breeding={breed}, "
                          f"Failed breeding={fail_breed}, "
                          f"Share={share} for {sheep_count}-Sheep __________")
                    # Continue to next sheep as this sheep has
                    # already interacted with a CS within action_dist.
                    continue 
                
                # S.1.3.1.3
                # If no sheep within action_dist but CS found within
                # s_min_dist, track and get closer to it while eating. 
                # This allows to get within action distance and at the same 
                # time, allows the sheep to stay closer like in a herd!
                elif closest_sheep != None:
                    print("->CS Found!")
                    print(f"-> {sheep_count}-Sheep ({i}) before moving "
                          f"closer (while eating) to "
                          f"CS-Sheep: ({closest_sheep}).")
                    # Call the run_to_closest_animal method from Parent class,
                    # eat method from Sheep class.
                    i.run_to_closest_animal(closest_sheep) # Works!
                    i.eat() # Eat while moving like in a herd!
                    print(f"-> {sheep_count}-Wolf ({i}) after moving closer "
                          f"(while eating) to CS-Sheep: ({closest_sheep}).")
                    print(f"___________ {sheep_count}-Sheep moved "
                          f"closer CS___________" )                   
                
                # S.1.3.1.4
                # If No CS found, but has store>s_min_energy, moves and eats.
                else:
                    print("-> NO CS Found.")
                    print(f"-> {sheep_count}-Sheep ({i}) before normally "
                          f"moving and eating.")
                    # Call the move and eat methods.
                    i.move()
                    i.eat()
                    print(f"-> {sheep_count}-Sheep ({i}) after normally "
                          f"moving and eating.")
                    print(f"...e1________ {sheep_count}-Sheep moved "
                          f"normally and ate ___________")
            
            # S.1.3.2
            # If store < s_min_energy, move and eat
            else:
                print(f"->{sheep_count}-Sheep has Store < "
                      f"Min_ernergy({s_min_energy}) ({i}). "
                      f"So moves and eat")
                print(f"-->{sheep_count}-Sheep ({i}) before normal moving "
                      f"and eating")
                # Call the move and eat methods.
                i.move()
                i.eat()
                print(f"-->{sheep_count}-Sheep ({i}) after normal moving "
                      f"and eating")
                print(f"___e2________ {sheep_count}-Sheep moved normally "
                      f"and ate ___________")
    
        # # Get list of store values for sheep
        # for i in range(len(sheep)):    
        #     # print(i, 'After', 'Store: ', sheep[i].store)
        #     # Adds store value to store_list
        #     store_list.append(sheep[i].store) 
        #     # print(store_list)     
        # # print(store_list)
        # # print(min(store_list))
    
        # S.1.4
        # The print below adds a space between two sheep printouts
        print('')  
        
    print('________________Sheep Cycle Ends_________________')
    print('________________Wolf Cycle Begins________________')
    
    # W.1
    # wolf_count: to assign the current wolf it's index value.
    wolf_count = -1 
    # wolf_index used to prevent comparison between same wolf/pair, 
    # used in j wolf slice as stratin index.
    wolf_index = 0 
    for i in wolves[:]:
        wolf_count += 1 # Assign the current wolf it's index value.
        wolf_index += 1 # Increase by 1 to prevent comparsion between same w/p.
        
        # W.1.1
        # The if conditon below: If wolf has > (high_store_mp) the minimum 
        # energy (store), its vision improves, meaning its proximity is 
        # multiplied by high_store_mp as wll.
        if i.store > min_energy*high_store_mp:
            min_dist = proximity*high_store_mp
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
        
        # W.1.2
        # 1. If (current wolf store <=min_energy) OR (store>min_energy AND  
        # p between bf_e/2 and <bf_e (which if bf_e not changed means,  
        # p is between 0.25 and <0.50)), then try find closest sheep (CS) to 
        # move closer to or if within action distance then eat. If no CS 
        # found, then just move randomly.
        # #Check if (current wolf store <=min_energy) OR (store>min_energy AND  
        # #p between bf_e/2 and <bf_e)
        if i.store <= min_energy or (i.store > min_energy and\
                        ((bf_e/2) <= random.random() < bf_e)):
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
            
            # W.1.2.1
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
                
                # W.1.2.1.A
                # If wolf find a CS within action distance: eats it!
                if distance <= action_dist:
                    # Eats the first CS sheep at action distance. 
                    # So should not loop through the other ones.
                    print(f"----> CS within {distance} which is "
                          f"<= action distance ({action_dist}).")
                    print(f"----> {wolf_count}-Wolf ({i}) before eating "
                          f"CS {sheep_count}-Sheep ({j})")
                    # Call the eat method from Wolf class.
                    i.eat(j) # Works!
                    print(f"----> {wolf_count}-Wolf ({i}) after eating "
                          f"CS {sheep_count}-Sheep ({j}).")
                    eaten = True # Set eat as true
                    # Eaten, so break (don't eat other CS within AD and 
                    # go to if below (and continue)
                    break 
                
                # W.1.2.1.B
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
            
            # W.1.2.2
            # Comes here from the break above if eaten = True.
            # Continue to next sheep.
            if eaten == True:
                print(f"___________ Eaten={eaten}. {wolf_count}-Wolf ate "
                      f"CS {sheep_count}-Sheep__________")
                # Move on to next wolf,as this wolf has already
                # already eaten a CS within action_dist, and so 
                # should not eat another CS if within action_dist
                continue
            
            # W.1.2.3
            # if CS found (but beyond action distance) within minimum
            # distance, chase it!
            elif closest_sheep != None:
                print("-> CS Found!")
                print(f"--> {wolf_count}-Wolf ({i}) before moving closer to "
                      f"CS ({closest_sheep }).")
                # Call the run_to_closest_animal from Parent class.
                i.run_to_closest_animal(closest_sheep) # Works!
                print(f"--> {wolf_count}-Wolf ({i}) after moving closer to "
                      f"CS ({closest_sheep }).")
                print(f"___________ {wolf_count}-Wolf moved closer "
                      f"to CS___________")           
            
            # W.1.2.4
            # If no CS found, wolf moves randomly based on move() method.
            else: 
                print("-> No CS found!")
                print(f"-->else1 begins: {wolf_count}-Wolf ({i}) "
                      f"before normal moving")
                # Call move method from Parent class.
                i.move()
                print(f"-->else1 ends: {wolf_count}-Wolf ({i}) "
                      f"after normal moving")
                print(f"....el1___________ {wolf_count}-Wolf moved "
                      f"normally___________") #el1 - keyword for debugging.
        
        # W.1.3
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
            
            # W.1.3.1
            # Slice is used as wolves might breed new wolves.
            # wolf_index is used as the starting index so that action is 
            # not duplicated for same wolf or same pair.
            for j in wolves[wolf_index:]:
                wolf2_count += 1 # Assign the other wolf it's index.
                print(f"---> {wolf_count}-Wolf looping with "
                      f"{wolf2_count}-Wolf")
                # Check distance between wolves
                distance =  i.dist_animals(j)
                
                # W.1.3.1.A
                # If a wolf between min_dist but beyond action_distance
                # assign it as the closest wolf and update minimum distance
                if action_dist < distance < min_dist: 
                    print('----> (AD2 < D < MD).')
                    min_dist = distance # Assign (and update if closer found)
                    closest_wolf = j # Assign (and update if closer found)
                    print(f"----> Min distance={min_dist} for "
                          f"{wolf_count}-Wolf ({i}) with "
                          f"{wolf2_count}-Wolf ({j})")  
                
                # W.1.3.1.B
                # If a wolf is within action distance: ACTION    
                elif distance <= action_dist:
                    print(f"----> d<=ad. breeding/fight roximity of "
                          f"{distance}(<={action_dist}) entered by "
                          f"{wolf_count}-Wolf ({i}) with CW "
                          f"{wolf2_count}-Wolf ({j}).")
                    
                    # W.1.3.1.B.1
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
                        # Call the breed_cost() method from Parent class.
                        breeding_cost = i.breed_cost(j)
                        # print('breeding_cost')
                        
                        # W.1.3.1.B.1.1
                        if random.random() > bf_e:
                            print(f"------>1.A. Random >{bf_e}. "
                                  f"So the wolves will mate.")
                            print(f"------> {wolf_count}-Wolf ({i}) before "
                                  f"mating with CW {wolf2_count}-Wolf ({j})")
                            i.store = breeding_cost
                            j.store = breeding_cost
                            wolves.append(af.Wolf(wolves, sheep,\
                                         environment, y=(i.y+5), x=(i.x+5)))
                            breed = True # Set breed as true!
                            print(f"------> Breed = {breed}")
                            print(f"------> {wolf_count}-Wolf ({i}) after "
                                  f"mating with CW {wolf2_count}-Wolf ({j})")
                            print(f"_____________ {wolf_count}-Wolf Mated "
                                  f"SUCCESSFULLY with "
                                  f"CW {wolf2_count}-Wolf ____________")
                        
                        # W.1.3.1.B.1.2    
                        else: # p <= bf_e
                            print(f"----->1.B. Random <{bf_e}. "
                                  f"So breeding will not be successful.")
                            print(f"----->{wolf_count}-Wolf ({i}) before "
                                  f"fail breeding with "
                                  f"CW {wolf2_count}-Wolf ({j})")
                            # Assign the new store values
                            i.store = breeding_cost
                            j.store = breeding_cost  
                            fail_breed = True # Set fail_breed as True
                            print(f"------> Fail Breeding = {fail_breed}")
                            print(f"_____________ {wolf_count}-Wolf ({i}) "
                                  f"after FAILED BREEDING with "
                                  f"CW {wolf2_count}-Wolf ({j})")
                        
                        # W.1.3.1.B.1.3
                        # Current wolf attempted breeding (successfully or 
                        # unsuccessfully) with the first CW. So should not 
                        # try with other CW even if within action distance.
                        # So break and go below to if and continue to next
                        # wolf.
                        break
                    
                    # W.1.3.1.B.2
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
                        
                        # W.1.3.1.B.2.1
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
                        
                        # W.1.3.1.B.2.2
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
                            print(f"------>{wolf_count}-Wolf ({i}) lost+moved"
                                  f" after fighting with CW "
                                  f"{wolf2_count}-Wolf ({j})")
                        
                        # W.1.3.1.B.2.3    
                        # Set fight as true for current wolf!    
                        fight = True 
                        print(f"------> Fight = {fight}")
                        print(f"_____________ {wolf_count}-Wolf Fought-(2) "
                              f"with CW {wolf2_count}-Wolf ____________")
                        # Current wolf already fought with CW within
                        # action distance. So break and go to below if 
                        # and continue to next wolf!
                        break
            
            # W.1.3.2        
            # If current wolf interacted with CW within action distance,
            # continue to the next wolf.
            if breed or fail_breed or fight == True:   
                print(f"_______ Breed={breed}, Failed Breed={fail_breed}, "
                      f"Fought={fight} for {wolf_count}-Wolf __________")
                continue
            
            # W.1.3.3
            # If CW found within min_distance but beyond action distance,
            # get close to it.
            elif closest_wolf != None:
                print("->CW Found!")
                print(f"-> {wolf_count}-Wolf ({i}) before moving closer to "
                      f"CW-Wolf: ({closest_wolf}).")
                # Call run_to_closest_animal() method from Parent class.
                i.run_to_closest_animal(closest_wolf) # Works!
                print(f"-> {wolf_count}-Wolf ({i}) after moving closer to "
                      f"CW-Wolf: ({closest_wolf}).")
                print(f"_______ {wolf_count}-Wolf moved closer CW+_______") 
            
            # W.1.3.4    
            # If No CW found, move as per the move method.
            else: # No CW. E>min_energy and p>bf_e
                print(f"-> No CW found. although store >{min_energy} and "
                      f"p>={bf_e}!")
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) before "
                      f"normal moving.")
                # Call move method from Parent class.
                i.move()
                print(f"--->else2 begins: {wolf_count}-Wolf ({i}) after "
                      f"normal moving.")
                print(f".... el2 _______  {wolf_count}-Wolf "
                      f"moved normally _______ ")
        
        # W.1.4
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
            # Call move method from Parent class.
            i.move()
            print(f"--->else3 begins: {wolf_count}-Wolf ({i}) after "
                  f"normal moving.")
            print(f"....e3_______ {wolf_count}-Wolf moved normally_______")
    print('________________Wolf Cycle Ends_________________')
    
    print('') # Add a blank space.
    # End timing calculation
    end = time.process_time() 
    # Print out the process time for each iteration:
    # print(f"Time to process iteration number: {it_no} is "
    #       f"{end - start} seconds.")
    # Calculate the total process time for the model. The print function
    # for this is at the end.
    global total_time
    for i in range(no_iterations):
            total_time += end-start
    print('')  # Add blank space.  
    print(f"*************** ITERATION NUMBER {it_no} ENDS ************")
    
    # Display environment, wolves and sheep!  
    plt.title("Sheep and Wolves Agent Based Model")
    plt.ylabel("Y Axis")
    plt.xlabel("X Axis")
    plt.ylim(0, len(environment))
    plt.xlim(0, len(environment[0])) 
    plt.imshow(environment)
    # sheep list, not no_sheep is used as no_sheep represents the initial 
    # number of sheep which may be altered via breeding or being eated 
    # by wolves. Same for wolves, as wolves might breed new wolves. 
    # Note, wovles do not die! So this may be improved, e.g. 
    # if wolf store < certain value.
    for i in range(len(sheep)):
        # If the color is removed, sheep and wolves will have different
        # colours at each iteration as their initialisation will be 
        # randomly determined by random shuffle. 
        plt.scatter(sheep[i].x, sheep[i].y, marker="p", color='white')
    for j in range(len(wolves)):
        plt.scatter(wolves[j].x, wolves[j].y, marker="v", color='black')
        
# Set up generator
def gen_function():
    """The generator function"""
    a = 0 # a compares with no_iterations to stop the generator.
    while a < no_iterations:
        yield a
        a += 1
 
# Set up run function for use with tkinter GUI
def run():
    """Runs the animation when Run button is clicked on GUI"""
    # animation = matplotlib.animation.FuncAnimation(fig, update,\
    # frames=gen_function, interval=100, repeat=False, save_count=no_iterations)
    animation = matplotlib.animation.FuncAnimation(fig, update,\
      frames=gen_function, repeat=False, save_count=no_iterations)
    
    # Save animation dsiabled as it might not work as for video as
    # ffmpeg might have to be installed manually. 
    # Writer = matplotlib.animation.writers['ffmpeg']
    # writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)
    # animation.save('ABM.mp4', writer=writer)
    # Gif disabled as well because I couldn't figure out how to display
    # and save as gif at the same time.
    # writergif = matplotlib.animation.PillowWriter(fps=60) 
    # animation.save('ABM.gif', writer=writergif)
    
    # .show() is deprecated.
    canvas.draw()
  
# Set up GUI
root = tkinter.Tk()
root.wm_iconbitmap('logo.ico')
root.wm_title("Sheep and Wolves ABM!")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Menu", menu=model_menu)
model_menu.add_command(label="Run ABM Model", command=run)
tkinter.mainloop()

# Write finished environment to a file:
with open('out.txt', 'w', newline='') as f2:     
   env_writer = csv.writer(f2)     
   for row in environment:         
        env_writer.writerow(row)

# Total store value of all sheep (https://bit.ly/3iMH5VW)
for i in range(len(sheep)):
        total_sheep_store += sheep[i].store
        # print(total_sheep_store)
# Transfer total_sheep_store to a t_sheep_store_list to be written in csv file
t_sheep_store_list.append(total_sheep_store) 
# print(t_sheep_store_list)
# Write the t_sheep_store_list in a csv file
with open('total_sheep_store.txt', 'a', newline='') as f3:     
    store_writer = csv.writer(f3, delimiter=' ')     
    store_writer.writerow(t_sheep_store_list)
    
# Total store value of all wolves
for i in range(len(wolves)):
        total_wolves_store += wolves[i].store
        # print(total_wolves_store)
# Transfer total_wolves_store to a t_wolves_store_list to be written 
# in csv file
t_wolves_store_list.append(total_wolves_store) 
# print(t_wolves_store_list)
# Write the t_wolves_store_list in a csv file
with open('total_wolves_store.txt', 'a', newline='') as f3:     
    store_writer = csv.writer(f3, delimiter=' ')     
    store_writer.writerow(t_wolves_store_list)
    
print('') #Add a blank space    
print(f"The model has run for {it_no} iterations,")
print(f"With {len(sheep)} sheep (total store: {total_sheep_store}),")
print(f"And {len(wolves)} wolves (total store: {total_wolves_store}),")
# print(f"And a total process time of {total_time} seconds.")
    
# # Close the prinout to log file! And return stdout to the 
# sys.stdout.close()
# sys.stdout = stdoutOrigin
