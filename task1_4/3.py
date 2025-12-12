# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 17:26:05 2025

@author: maalv
"""

t = int(input())

for _ in range(t):
    line = input().split()
    n = int(line[0])
    d = line[1] 
    
    number_str = input().strip()

    inserted = False
    result_list = []

    for digit in number_str:
        if not inserted and d > digit:
            result_list.append(d)
            inserted = True
        result_list.append(digit)
    if not inserted:
        result_list.append(d)
    print("".join(result_list))