#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 02:27:17 2018

@author: siwen_chen
"""

import cv2
from matplotlib import pyplot as plt
from IPython.core.pylabtools import figsize
from random import randint
import segment_function
import cal_IOU
from scipy import misc

#import turnin_points

import os
import order
import writeinexcel

#image path
#path1 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/dataset/tracking/samples/sample1-HannoNIR880603'
#path1 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/dataset/tracking/samples/sample2-HannoNIR880683'
path1 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/dataset/tracking/samples/sample3-HannoNIR880743'
#path1 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/dataset/tracking/samples/sample4-HannoNIR880613'
#path1 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/dataset/tracking/samples/sample5-HannoNIR880673'

#result save path
#path2 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample1-HannoNIR880603'
#path2 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample2-HannoNIR880683'
path2 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample3-HannoNIR880743'
#path2 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample4-HannoNIR880613'
#path2 = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample5-HannoNIR880673'

all_pics_name = os.listdir(path1)
all_pics_name.sort(key= lambda x:int(x[:-4]))
    
#limit to frames apart
frames_apart = 5

#limit to similarity ratio -- d
IOU_threshold = 0.5



IOU_list = []
imgs_to_draw = []
pic_contrs = []
for contr in range(len(all_pics_name)):
    pic_path = path1 + '/' + all_pics_name[contr]
    number = int(all_pics_name[contr][0:2])
    vec_sample_dist,value_hsv,canny_low_threshold,threshold_IOU,min_contour_length,vector_angle_low_threshold,vector_angle_high_threshold,threshold_seg_dist = writeinexcel.read_parameter(number+1)
    pic_contour_list = segment_function.leaf_segment(pic_path,int(vec_sample_dist),int(value_hsv),int(canny_low_threshold),threshold_IOU,int(min_contour_length),vector_angle_low_threshold,vector_angle_high_threshold,threshold_seg_dist)  
    img = cv2.imread(pic_path)
    imgs_to_draw.append(img)
    pic_contrs.append(pic_contour_list)  



for ant in range(len(all_pics_name)-1):   # ant + 1 = picture name

    if ant + frames_apart > len(all_pics_name) :
        frames_apart = frames_apart - 1
    
    fix_pic_path = path1 + '/' + all_pics_name[ant]
    
#    fix_pic_contour_list = segment_function.leaf_segment(fix_pic_path)
    fix_pic_contour_list = pic_contrs[ant]
    
    for bnt in range(ant + 1, ant + frames_apart):
        test_pic_path = path1 + '/' + all_pics_name[bnt]
        
#        test_pic_contour_list = segment_function.leaf_segment(test_pic_path)
        test_pic_contour_list = pic_contrs[bnt]
        
        #loop for IOU list
        for cnt in range(len(fix_pic_contour_list)):
            fixpic_seg = fix_pic_contour_list[cnt]
            fixpic_seg_shape_img = cal_IOU.shape1(fix_pic_path,fixpic_seg)
           
            for dnt in range(len(test_pic_contour_list)):
                testpic_seg = test_pic_contour_list[dnt]
                testpic_seg_shape_img = cal_IOU.shape1(fix_pic_path,testpic_seg)
                
                track_IOU = cal_IOU.cal_IOU1(fixpic_seg_shape_img,testpic_seg_shape_img)
                if track_IOU >= IOU_threshold:
                    track_or_not = (track_IOU,'fixpic:',(ant,cnt),'test_pic:',(bnt,dnt))
                    IOU_list.append(track_or_not)
                    print(track_or_not)
                    
                    test_img = cv2.imread(test_pic_path)
                    for ent in fixpic_seg:
                        cv2.drawContours(test_img,[ent],-1,(255,0,0),2)
                    for fnt in testpic_seg:
                        cv2.drawContours(test_img,[fnt],-1,(0,255,0),2)
                    plt.imshow(test_img)
                    plt.show()
          
#print(IOU_list)                   

IOU_descending_list = order.descending_order(IOU_list)
print('IOU_descending_list:',IOU_descending_list)

seg_pairs = []
for gnt in range(len(IOU_descending_list)):
    pairs = [IOU_descending_list[gnt][-3],IOU_descending_list[gnt][-1]]
    seg_pairs.append(pairs)
print('seg_pairs:',seg_pairs)

track_segs_list = [seg_pairs[0]]
for hnt in range(1,len(seg_pairs)):
    to_group_pair = seg_pairs[hnt]  #to_group_pair shapes like [(2,3),(5,7)]
    
    to_group_leaf1_grouped_or_not = False   
    for jnt in range(len(track_segs_list)):
        track_group_for_leaf1 = track_segs_list[jnt]   #track_group shapes like [(2,4),(3,5),(3,7),(3,6)...]        
        for track_group_member_for_leaf1 in track_group_for_leaf1:   #track_group_member shapes like (2,4)                             
            
            
            if to_group_pair[0] == track_group_member_for_leaf1:
                to_group_leaf1_grouped_or_not = True                                
                
                to_group_leaf2_grouped_or_not = False                    
                for lnt in range(jnt,len(track_segs_list)):  #test the other leaf grouped or not
                    track_group_for_leaf2 = track_segs_list[lnt]                    
                    for track_group_member_for_leaf2 in track_group_for_leaf2:  # track_group_member2 shapes like (2,4)
                        if to_group_pair[1] == track_group_member_for_leaf2:                            
                            to_group_leaf2_grouped_or_not = True

                            from_same_pic_ornot = False                            
                            #check if two track groups have leaves from same pic
                            for mnt in track_group_for_leaf1:
                                for nnt in track_group_for_leaf2:
                                    if mnt[0] == nnt[0]:                                        
                                        from_same_pic_ornot = True
                                        print('track_group_for_leaf1:',mnt,'track_group_for_leaf2:',nnt)
                            #如果没有同一图片的leaf，合并两组            
                            if from_same_pic_ornot == False:
                                track_segs_list[jnt].append(track_group_for_leaf2)
                                del track_segs_list[lnt]
                                break
                            break
                        break
                    break
                        
                if to_group_leaf2_grouped_or_not == False:
                    track_segs_list[jnt].append(to_group_pair[1])
                    break
                break

            if to_group_pair[1] == track_group_member_for_leaf1:                
                to_group_leaf1_grouped_or_not = True
                
                to_group_leaf2_grouped_or_not_2 = False
                for ont in range(jnt,len(track_segs_list)):  #test the other leaf grouped or not
                    track_group_for_leaf2_2 = track_segs_list[ont]
                    for track_group_member_for_leaf2_2 in track_group_for_leaf2_2:  # track_group_member2 shapes like (2,4)
                        if to_group_pair[0] == track_group_member_for_leaf2_2:                            
                            to_group_leaf2_grouped_or_not_2 = True
                            
                            from_same_pic_ornot = False                            
                            #check if two track groups have leaves from same pic
                            for pnt in track_group_for_leaf1:
                                for qnt in track_group_for_leaf2_2:
                                    if pnt[0] == qnt[0]:
                                        from_same_pic_ornot = True
                                        print('track_group_for_leaf1:',pnt,'track_group_for_leaf2_2:',qnt)

                            if from_same_pic_ornot == False:
                                track_segs_list[jnt].append(track_group_for_leaf2_2)
                                del track_segs_list[ont]
                                break
                            break
                        break
                    break
                        
                if to_group_leaf2_grouped_or_not_2 == False:
                    track_segs_list[jnt].append(to_group_pair[0])
                    break
                break
            
    if to_group_leaf1_grouped_or_not == False:
        track_segs_list.append(to_group_pair)

print('track_segs_list:',track_segs_list)

track_segs_list_1 = []
for track_list_member in track_segs_list:
    track_list_member_1 = list(set(track_list_member))
    track_segs_list_1.append(track_list_member_1)

b = len(track_segs_list_1)
for i in range(b):
    for j in range(b):
        x = list(set(track_segs_list_1[i]+track_segs_list_1[j]))
#        print(x)
        y = len(track_segs_list_1[j])+len(track_segs_list_1[i])
#        print(y)
        if i == j or track_segs_list_1[i] == [26] or track_segs_list_1[j] == [26]:
            break
        elif len(x) < y:
            track_segs_list_1[i] = x
            track_segs_list_1[j] = [(26,0)]
#            print('a:',track_segs_list_1)
print('final:',[i for i in track_segs_list_1 if i != [(26,0)]])  


for track_group_plus in [i for i in track_segs_list_1 if i != [(26,0)]]:
    col = (randint(0,255),randint(0,255),randint(0,255))
    for knt in range(len(track_group_plus)):
        track_seg = track_group_plus[knt]
        pic_numbr = track_seg[0]
        seg_numbr = track_seg[1]
        cv2.drawContours(imgs_to_draw[pic_numbr],pic_contrs[pic_numbr][seg_numbr],-1,col,2)
    
names = []
for nr in range(len(imgs_to_draw)):
    nr_str = '%s'% nr
    names.append(nr_str)


for nrstr in names:
    misc.imsave(path2 + '/' + nrstr + '.png', imgs_to_draw[int(nrstr)])
    figsize(20,20)
    plt.imshow(imgs_to_draw[int(nrstr)])
    plt.show()     
    
# =============================================================================
#      for tracking example showed in report
# =============================================================================
#color = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(randint(0,255),randint(0,255),randint(0,255)),(randint(0,255),randint(0,255),randint(0,255)),(randint(0,255),randint(0,255),randint(0,255)),(randint(0,255),randint(0,255),randint(0,255))]
#n = 0
#for track_group_plus in [i for i in track_segs_list_1 if i != [(26,0)]]:
#    col = color[n]
#    for knt in range(len(track_group_plus)):
#        track_seg = track_group_plus[knt]
#        pic_numbr = track_seg[0]
#        seg_numbr = track_seg[1]
#        cv2.drawContours(imgs_to_draw[pic_numbr],pic_contrs[pic_numbr][seg_numbr],-1,col,10)
#    n = n + 1
#
#names = []
#for nr in range(len(imgs_to_draw)):
#    nr_str = '%s'% nr
#    names.append(nr_str)
#
#
#for nrstr in names:
#    misc.imsave(path2 + '/' + nrstr + '.png', imgs_to_draw[int(nrstr)])
#    figsize(20,20)
#    plt.imshow(imgs_to_draw[int(nrstr)])
#    plt.show()