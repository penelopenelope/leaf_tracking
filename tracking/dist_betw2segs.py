#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 04:35:34 2018

@author: siwen_chen
"""

import numpy as np

def eucldist(p1,p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    eucldist = np.sqrt(x**2 + y**2)
    return eucldist


def dist_between_two_segs(tips1,tips2):
    dis11 = eucldist(tips1[0],tips2[0])
    dis12 = eucldist(tips1[0],tips2[1])
    dis21 = eucldist(tips1[1],tips2[0])
    dis22 = eucldist(tips1[1],tips2[1])
    if dis11 == min(dis11,dis12,dis21,dis22):
        return dis11,tips1[1],tips2[1]     #return the left two tips(unconnected)
    if dis12 == min(dis11,dis12,dis21,dis22):
        return dis12,tips1[1],tips2[0]
    if dis21 == min(dis11,dis12,dis21,dis22):
        return dis21,tips1[0],tips2[1]
    if dis22 == min(dis11,dis12,dis21,dis22):
        return dis22,tips1[0],tips2[0]
