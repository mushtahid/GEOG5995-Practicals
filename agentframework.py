# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 08:37:16 2020

@author: Mushtahid
"""

import random
# random.seed(10)

class Agent:
     # Put none in x and y (https://bit.ly/3d7tqY9)?
    def __init__(self, environment, agents, y=None, x=None):
        if (y == None):
            self.y = random.randint(0,len(environment))
        else:
            self.y = y
        if (x == None):
            self.x = random.randint(0,len(environment[0]))
        else:
            self.x = x
        self.environment = environment
        self.agents = agents # Include list of agents inside agents
        self.store = 0 
        
    def move(self):
        if random.random() < 0.5:
            self.y = (self.y + 1) % 100
        else:
            self.y = (self.y - 1) % 100

        if random.random() < 0.5:
            self.x = (self.x + 1) % 100
        else:
            self.x = (self.x - 1) % 100

    def eat(self): # can you make it eat what is left?
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        # Eating what is left
        else:
            self.environment[self.y][self.x] -= self.environment[self.y][self.x]
            self.store += self.environment[self.y][self.x]

    def distance_between(self, agent):
        """ Calculate and return distance between agents """
        return (((self.y - agent.y)**2) + ((self.x - agent.x)**2))**0.5           
             
    def share_with_neighbours(self, neighbourhood):
        """ If other agents within 20, share resrouces """
        #self.neighbourhood = neighbourhood # Do I need this?
        for agent in self.agents:
            distance = self.distance_between(agent)
            if distance <= neighbourhood:
                average = ((self.store + agent.store)/2)
                self.store = average
                agent.store = average
                print("sharing " + str(distance) + " " + str(average))
    

    
    #Overriding standard methods (https://bit.ly/34Ih3hC, https://bit.ly/3iMH5VW)
    def __str__(self):
        return f"Agent location: (y={self.y},x={self.x}). Store value: {self.store}"





