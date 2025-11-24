# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 20:12:58 2025

@author: maalv
"""
import math

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
