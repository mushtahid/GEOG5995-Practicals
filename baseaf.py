# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 08:37:16 2020

@author: Mushtahid
"""

import random
random.seed(10)

class Agent:
     # Put None as default in x and y (https://bit.ly/3d7tqY9)
    def __init__(self, environment, agents, wolves, y = None, x = None):
        if (y == None):
            self.y = random.randint(0, len(environment))
        else:
            self.y = y
        if (x == None):
            self.x = random.randint(0, len(environment[0]))
        else:
            self.x = x
        self.environment = environment
        self.agents = agents
        self.wolves = wolves
        self.store = 0 
        
    def move(self):
        """ Move agents based on random and store value """
        if 250 < self.store <500:
            if random.random() < 0.5:
                self.y = (self.y + 3) % (len(self.environment))
            else:
                self.y = (self.y - 3) % (len(self.environment))
            if random.random() < 0.5:
                self.x = (self.x + 3) % (len(self.environment[0]))
            else:
                self.x = (self.x - 3) % (len(self.environment[0]))
        elif self.store > 500:
            if random.random() < 0.5:
                self.y = (self.y + 7) % (len(self.environment))
            else:
                self.y = (self.y - 7) % (len(self.environment))
            if random.random() < 0.5:
                self.x = (self.x + 7) % (len(self.environment[0]))
            else:
                self.x = (self.x - 7) % (len(self.environment[0]))
        else:
            if random.random() < 0.5:
                self.y = (self.y + 1) % (len(self.environment))
            else:
                self.y = (self.y - 1) % (len(self.environment))
            if random.random() < 0.5:
                self.x = (self.x + 1) % (len(self.environment[0]))
            else:
                self.x = (self.x - 1) % (len(self.environment[0]))

    def eat(self): # can you make it eat what is left?
        """ Make agents eat environment """
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        # Eating what is left (https://bit.ly/3iMH5VW)
        else:
            self.environment[self.y][self.x] -= self.environment[self.y][self.x]
            self.store += self.environment[self.y][self.x]
    
    def vomit(self):
        """ Make agents vomit 250 stores if they have eaten more than 950 """
        if self.store > 950:
            self.store -= 250
            self.environment[self.y][self.x] += 250
            
    def distance_between(self, agent):
        """ Calculate and return distance between agents """
        return (((self.y - agent.y)**2) + ((self.x - agent.x)**2))**0.5           

    def share_with_neighbours(self, neighbourhood):
        """ If agents within 30 distance, either steal or share average store """
        # self.neighbourhood = neighbourhood # Not needed.
        for agent in self.agents:
            distance = self.distance_between(agent)
            if distance <= neighbourhood:
                average = ((self.store + agent.store)/2)       
                # If self.store is less than 95% of agent.store
                    # Steal that % from agent.store. eg. if 50% then steal 50%
                # Else just share the average
                if self.store < (0.95*agent.store):
                    store_div = self.store/agent.store
                    self.store += (store_div*agent.store)
                    agent.store -= (store_div*agent.store)
                else:
                    self.store = average
                    agent.store = average
                # print (f"Sharing Dist: {distance}. Store Avg: {average}")            
                  
    # Overriding standard methods (https://bit.ly/34Ih3hC, https://bit.ly/3iMH5VW)
    def __str__(self):
        return f"Agent location: (y={self.y},x={self.x}), Store: {self.store}"

class Wolf:

    def __init__(self, environment, wolves, agents, y, x):
            self.y = random.randint(0, len(environment))
            self.x = random.randint(0, len(environment[0]))
            self.environment = environment
            self.wolves = wolves
            self.agents = agents
    
    def move_wolves(self):
        if random.random() < 0.5:
            self.y = (self.y + 5) % (len(self.environment))
        else:
            self.y = (self.y - 5) % (len(self.environment))
        if random.random() < 0.5:
            self.x = (self.x + 5) % (len(self.environment[0]))
        else:
            self.x = (self.x - 5) % (len(self.environment[0]))
    
    # def distance_between(self, agent):
    #     """ Calculate and return distance between agents """
    #     return (((self.y - agent.y)**2) + ((self.x - agent.x)**2))**0.5           
    
    # def dist_ws (self): # Did not work
    #     # for agent in self.agents:
    #     #     distance = self.distance_between(agent)
    #     #     print(agent, distance)
    #     for wolf in self.wolves:
    #         distance = self.distance_between(wolf)
    #         print(wolf, distance)

    # def eat_sheep(self):
    #     pass
    
    # def __str__(self):
        # return f"Wolf location: (y={self.y},x={self.x}), Distance: {distance}"
