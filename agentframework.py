# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 08:37:16 2020

@author: Mushtahid
"""

import random

class Agent:
    def __init__(self, environment, agents):
        self.x = random.randint(0,99)
        self.y = random.randint(0,99)
        self.environment = environment
        self.agents = agents # Include list of agents inside agents
        self.store = 0 # We'll come to this in a second.
        
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
             
    def share_with_neighbours(self, neighbourhood):
        self.neighbourhood = neighbourhood
        for agent in self.agents:
            distance = self.distance_between(agent)
            if distance <= neighbourhood:
                average = ((self.store + agent.store)/2)
                self.store = average
                agent.store = average
                print("sharing " + str(distance) + " " + str(average))
    
    def distance_between(self, agent):
        """
        Calculate and returns the distance between agents a and b.
        ----------
        a : TYPE
            DESCRIPTION.
            b : TYPE
            DESCRIPTION.

        Returns
        -------
        Distance between agents a and b.
        """
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5    





