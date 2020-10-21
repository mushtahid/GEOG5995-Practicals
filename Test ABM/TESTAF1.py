# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:20:41 2020

@author: Mushtahid
"""
import random
# random.seed(10)

class Animal:
    
    def __init__(self, animals, wolves, sheep, environment, y=None, x=None):
        self.animals = animals # need to delete later
        self.wolves = wolves
        self.sheep = sheep
        self.environment = environment
        if (y == None):
            self.y = random.randint(0, len(environment)-2)
        else:
            self.y = y
        if (x == None):
            self.x = random.randint(0, len(environment[0])-2)
        else:
            self.x = x  
        # self.y = random.randint(0, len(environment))
        # self.x = random.randint(0, len(environment[0]))
        # Set initial store value based on probability
        if random.random() < 0.25:
            self.store = 100
        elif 0.25 <= random.random() < 0.50:
            self.store = 200
        elif 0.50 <= random.random() < 0.75:
            self.store = 300
        else:
            self.store = 400

    def dist_animals(self, animal):
        return (((self.y - animal.y)**2) + ((self.x - animal.x)**2))**0.5

    def boundary_conditons(self):
        if self.y >= len(self.environment):
            self.y = len(self.environment)-2
        elif self.y <= 0:
            self.y = 2
        if self.x >= len(self.environment[0]):
            self.x = len(self.environment[0])-2
        elif self.x <= 0:
            self.x = 2

    def move(self):
        if random.random() < 0.5:
            self.y += 1
        else:
            self.y -= 1
        if random.random() < 0.5:
            self.x += 1
        else:
            self.x -= 1
                
        self.boundary_conditons()
    
    def __str__(self):
        return f"y={self.y}, x={self.x}, store={self.store}"
    
class Sheep(Animal):

    def eat(self):
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        else:
            self.environment[self.y][self.x] -= self.environment[self.y][self.x]
            self.store += self.environment[self.y][self.x]
            
class Wolf(Animal):
    pass
    
    # def eat(self, proximity, i):
    #     sheep_count = -1
    #     for j in self.sheep[:]:
    #         sheep_count += 1
    #         distance = self.dist_animals(j)
    #         # print(f"wolf{i}: {wolves[i].y},{wolves[i].x}, sheep{j}: {sheep[j].y},{sheep[j].x}, d={distance}")
    #         print(f"Wolf {i} {self.y},{self.x}, sheep: {sheep_count} {j.y},{j.x}, d={distance}")
    #         if distance < proximity:
    #             self.store += j.store
    #             print(f"Sheep {sheep_count} {j} eaten by Wolf {i}")
    #             j.store = 0
    #             self.sheep.remove(j)
    #             break
