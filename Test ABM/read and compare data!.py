# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 20:05:55 2020

@author: User
"""

import csv

before_oop = []
testmodel_1 = []

# Read before_oop 
with open('log2.txt', newline='') as f:
    r = csv.reader(f)
    for row in r:
        row_list = []
        for value in row:
            row_list.append(value)
        before_oop.append(row_list)
        
# Read testmodel_1
with open('log.txt', newline='') as f:
    r = csv.reader(f)
    for row in r:
        row_list = []
        for value in row:
            row_list.append(value)
        testmodel_1.append(row_list)
        
# Check if both have same content
print('Same:',before_oop == testmodel_1) #If true then same