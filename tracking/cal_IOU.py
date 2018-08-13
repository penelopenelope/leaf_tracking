#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 04:40:53 2018

@author: siwen_chen
"""
import cv2
import numpy as np
import lsf_circlefit

def img_info(path):
    img = cv2.imread(path)
    height,width,channels = img.shape 
    return img,height,width

def shape(path,all_cntr,new_seg):
    img,height,width = img_info(path)
    img1 = np.zeros((height,width),np.uint8)
    for pnt in new_seg:
        x,y,radius = lsf_circlefit.lsf_circle(np.array(all_cntr[pnt]))
        center = (int(x),int(y))
        radius = int(radius)
        img1 = cv2.circle(img1,center,radius,(255,0,0),-1)    
#    plt.imshow(img1)
#    plt.show()
    return img1

def shape1(path,segs):
    img,height,width = img_info(path)
    img1 = np.zeros((height,width),np.uint8)
    for seg in segs:
        x,y,radius = lsf_circlefit.lsf_circle(seg)
        center = (int(x),int(y))
        radius = int(radius)
        img1 = cv2.circle(img1,center,radius,(255,0,0),-1)
    
    return img1

def circle_img(path,cntr):  
    img,height,width = img_info(path)
    img1 = np.zeros((height,width),np.uint8)
    img1 = cv2.drawContours(img1,[np.array(cntr)],0,1,1)
    x,y,radius = lsf_circlefit.lsf_circle(np.array(cntr))
    center = (int(x),int(y))
    radius = int(radius)
    img1 = cv2.circle(img1,center,radius,(255,0,0),-1)        
    return img1,radius

def cal_IOU(path,non_circle_img,contours_to_add):
    img,radius = circle_img(path,contours_to_add)
#    non_circle_area = int(np.sum(non_circle_img)/255)
    intersect = np.logical_and(non_circle_img,img)
    union = np.logical_or(non_circle_img,img)
    area_intersect = np.sum(intersect)
    area_union = np.sum(union)
    IOU = area_intersect/area_union           
    return IOU

def cal_IOU1(shape_img1,shape_img2):
    intersect = np.logical_and(shape_img1,shape_img2)
    union = np.logical_or(shape_img1,shape_img2)
    area_intersect = np.sum(intersect)
    area_union = np.sum(union)
    IOU = area_intersect/area_union
    return IOU