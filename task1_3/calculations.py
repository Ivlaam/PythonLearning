# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 20:12:58 2025

@author: maalv
"""
import math

def optimal (rel): # d1 - 0, d2 - 1, h - 2, vsand - 3, n - 4, th - 5
    step = 0.1 
    best_time = 999999999.999
    optim_degree = 0.0
    opt = []
    
    for start_angle in [i * step for i in range (int(90/step)+1)]:
        start_rad = math.radians(start_angle)
        h_water = rel[0]*math.tan(start_rad)
        if h_water >= rel[2]:
            continue
        
        l1 = math.sqrt(h_water**2 + rel[0]**2)
        
        h_remaining = rel[2] - h_water
        l2 = math.sqrt(h_remaining**2 + rel[1]**2)
        
        current_time = (1/rel[3])*(l1+rel[4]*l2)
        if current_time < best_time:
            best_time = current_time
            optim_degree = start_angle
    opt.append(optim_degree)
    opt.append(best_time)
    return opt

#changing strings to float, yards to feet, mph to yards per second
def rearrange (d1, d2, h, vsand, n, th):
    rel = []
    d1 = float(d1)*3
    rel.append(d1)                  #0
    d2 = float(d2)                      
    rel.append(d2)                  #1
    h = float(h)*3
    rel.append(h)                   #2
    vsand = float(vsand)*5280/3600
    rel.append(vsand)               #3
    n = float(n)
    rel.append(n)                   #4
    th = float(th)
    rel.append(th)                  #5
    return rel

def calc (rel):
    rad = math.radians(rel[5])
    x = rel[0] * math.tan(rad)
    l1 = math.sqrt(x**2+rel[0]**2)
    l2 = math.sqrt((rel[2]-x)**2+rel[1]**2)
    t = (1/rel[3])*(l1+rel[4]*l2)
    return t
