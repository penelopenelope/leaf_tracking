#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:52:06 2018

@author: siwen_chen
"""


def descending_order(listt):
    descending_list = sorted(listt,key = lambda l:l[0], reverse = True)
    return descending_list

def compr(a,b):
    flag = False
    for aa in a:
        for bb in b:
            if aa == bb:
                flag = True
    return flag

def find_finalcomb(a):
    b = len(a)
    for i in range(b):
        for j in range(b):
            x = list(set(a[i]+a[j]))
            y = len(a[j])+len(a[i])
            if i == j or a[i] == 0 or a[j] == 0:
                break
            elif len(x) < y:
                a[i] = x
                a[j] = [0]
    return [i for i in a if i != [0]]