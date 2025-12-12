# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 17:43:37 2025

@author: maalv
"""

n = int(input())
a = list(map(int, input().split()))

total_sum = sum(a)

if total_sum != 0:
    print("YES")
    print(1)
    print(1, n)
else:
    prefix_sum = 0
    split_index = -1
    for i in range(n):
        prefix_sum += a[i]
        if prefix_sum != 0:
            split_index = i + 1
            break
    if split_index != -1 and split_index < n:
        print("YES")
        print(2)
        print(1, split_index)
        print(split_index + 1, n)
    else:
        print("NO")