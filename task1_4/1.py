# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 16:11:38 2025

@author: maalv
"""
a=int(input())
for i in range(a):
    b=int(input())
    l=list(map(int,input().split()))
    mn=min(l)
    l.remove(mn)
    s=1
    for j in l:
        s*=j
    print(s*(mn+1))
    s=1