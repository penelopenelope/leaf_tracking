#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 01:22:47 2018

@author: siwen_chen
"""
import math

def lsf_circle(points):  
    N =len(points) 
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    sum_x3 = 0
    sum_y3 = 0
    sum_xy = 0
    sum_x1y2 = 0
    sum_x2y1 = 0

    for  i in range(N) :
#        print(points[i][0])
        x = float(points[i][0][0])
        y = float(points[i][0][1])        
        x2 = x * x
        y2 = y * y
        sum_x = sum_x + x
        sum_y = sum_y + y
        sum_x2 = sum_x2 + x2
        sum_y2 = sum_y2 + y2
        sum_x3 = x * x2 + sum_x3
        sum_y3 = y * y2 + sum_y3
        sum_xy = x * y + sum_xy
        sum_x1y2 = x * y2 + sum_x1y2
        sum_x2y1 = x2 * y + sum_x2y1  
    C = N * sum_x2 - sum_x * sum_x
    D = N * sum_xy - sum_x * sum_y
    E = N * sum_x3 + N * sum_x1y2 - (sum_x2 + sum_y2) * sum_x
    G = N * sum_y2 - sum_y * sum_y
    H = N * sum_x2y1 + N * sum_y3 - (sum_x2 + sum_y2) * sum_y
    a = (H * D - E * G) / (C * G - D * D+1e-100)
    b = (H * C - E * D) / (D * D - G * C+1e-100)
    c = -(a * sum_x + b * sum_y + sum_x2 + sum_y2) / N
    centerx = a / (-2)
    centery = b / (-2)
    rad = math.sqrt(a * a + b * b - 4 * c) / 2

    return centerx,centery,rad