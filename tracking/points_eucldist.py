#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 02:28:31 2018

@author: siwen_chen
"""
import numpy as np
def eucldist(p1,p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    eucldist = np.sqrt(x**2 + y**2)
    return eucldist
