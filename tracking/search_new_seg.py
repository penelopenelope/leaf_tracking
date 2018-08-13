#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 21:35:07 2018

@author: siwen_chen
"""

import numpy as np

#contout sample for test
#a =  ([( 99, 24), ( 99, 25), ( 99, 26), ( 99, 27), ( 99, 28), ( 99, 29),
#       ( 99, 30), (100, 22), (100, 23), (100, 31), (100, 32), (100, 33),
#       (101, 21), (102, 20), (103, 19), (104, 18), (105, 18), (105, 41),
#       (106, 17), (106, 42), (107, 17), (107, 43), (107, 44), (108, 16),
#       (108, 45), (109, 16), (109, 46), (110, 16), (110, 47), (111, 15),
#       (111, 48), (112, 15), (112, 48), (113, 15), (113, 49), (114, 15),
#       (114, 49), (115, 15), (115, 49), (116, 15), (116, 49), (117, 15),
#       (117, 49), (118, 15), (118, 49), (119, 15), (119, 49), (120, 15),
#       (120, 49), (121, 15), (121, 49), (122, 16), (122, 49), (123, 16),
#       (123, 48), (124, 16), (124, 47), (125, 16), (125, 47), (126, 17),
#       (126, 47), (127, 17), (127, 46), (128, 18), (128, 45), (129, 19),
#       (129, 45), (130, 19), (130, 44), (131, 20), (131, 43), (132, 21),
#       (132, 22), (132, 42), (133, 23), (133, 40), (133, 41), (134, 24),
#       (134, 25), (134, 39), (135, 26), (135, 27), (135, 28), (135, 36),
#       (135, 37), (135, 38), (136, 29), (136, 30), (136, 31), (136, 32),
#       (136, 33), (136, 34), (136, 35)])
#
#b = ([(33, 18), (33, 19), (33, 20), (33, 21), (33, 22), (33, 23),
#       (33, 24), (33, 25), (34, 17), (34, 26), (34, 27), (35, 16),
#       (35, 28), (36, 15), (37, 14), (38, 13), (39, 12), (40, 11),
#       (41, 11), (42, 11), (43, 11), (44, 11), (45, 11), (46, 11),
#       (47, 11), (48, 11), (49, 11), (50, 12), (51, 13), (52, 13),
#       (53, 14), (54, 15), (55, 16), (55, 17), (55, 26), (55, 27),
#       (55, 28), (55, 29), (55, 30), (55, 31), (56, 18), (56, 19),
#       (56, 20), (56, 21), (56, 22), (56, 23), (56, 24), (56, 25),
#       (56, 32), (56, 33), (57, 34), (57, 35)])

import find_tips2
import dist_betw2segs
import cal_IOU

def find_new_seg(path,contour_list,position,fixed_con_origin_circle_img,fixed_con_tips):
    __,height,width = cal_IOU.img_info(path)
    search_range = contour_list[position+1:]
    dist = []
    fixed_con = contour_list[position]
    flag = False
    nnew_seg = []
    nnew_tips = []
    nnew_shape = []
    closest_con_pos_in_contour3count = 0
    nnew_seg.append(fixed_con)    
    for test in range(len(search_range)):
        test_con = search_range[test]
        test_con_tips = find_tips2.find_tips(test_con)
        if test_con_tips == [] or len(test_con_tips) <= 1:
            break
        per_dist,__,__ = dist_betw2segs.dist_between_two_segs(fixed_con_tips,test_con_tips)
        dist.append(per_dist)
        if min(dist) <= 10 and min(dist) != 0:
            closest_con_pos_in_dist = dist.index(min(dist))
            closest_con_pos_in_contour3count = closest_con_pos_in_dist + position + 1
            closest_con = contour_list[closest_con_pos_in_contour3count]
            
#show closest seg pairs
#            ppp = np.zeros((height,width),np.uint8)
#            ppp1 = ppp.copy()
#            ppp2 = ppp.copy()
#            plt.title('fixed_con')
#            cv2.drawContours(ppp,[fixed_con],0,1,1)
#            plt.imshow(ppp)
#            plt.show()
#            plt.title('closest_con')
#            cv2.drawContours(ppp1,[closest_con],0,1,1)
#            plt.imshow(ppp1)
#            plt.show()
            
            IOU = cal_IOU.cal_IOU(path,fixed_con_origin_circle_img,closest_con)
            
    #        print(IOU)
    #        print(dist)
    
            if IOU != 0:
                
    #            nnew_seg = np.concatenate((fixed_con,closest_con),axis=0)
                nnew_seg.append(closest_con)
                
                #show the new seg
#                for ff in range(len(nnew_seg)):
#                    cv2.drawContours(ppp2,[nnew_seg[ff]],-1,1,1)
#                plt.title('new_seg_in_function')
#                plt.imshow(ppp2)
#                plt.show()
                
                nnew_tips = new_seg_tips(fixed_con_tips,closest_con,nnew_seg)
                nnew_shape = new_seg_shape(path,fixed_con_origin_circle_img,closest_con)
                flag = True
                if len(nnew_tips) == 1:
                    flag = False
    return flag,nnew_seg,nnew_tips,nnew_shape,closest_con_pos_in_contour3count


def new_seg_shape(path,non_circle_img,seg_to_add):
    img_to_add,radius = cal_IOU.circle_img(path,seg_to_add)
    new_shape_img = np.logical_or(non_circle_img,img_to_add)
#    new_shape_area = cal_IOU.cal_area(new_shape_img)
    return new_shape_img


def new_seg_tips(fixed_con_tips,seg2,new_seg):
    tips2 = find_tips2.find_tips(seg2)
    __,link_tip1,link_tip2 = dist_betw2segs.dist_between_two_segs(fixed_con_tips,tips2)
#    found_tips = find_tips2.find_tips(new_seg)
    found_tips = []
    found_tips.extend(fixed_con_tips)
    found_tips.extend(tips2)
        
    new_tips = []
    for tip in range(len(found_tips)):
        if found_tips[tip] != link_tip1 and found_tips[tip] != link_tip2:
            new_tips.append(found_tips[tip])
    return new_tips


def con3_incount(cntr,min_contour_length):
    con3count_pos_in_con3 = []
    contours3_in_count = []
    for cnt in range(len(cntr)):
        if len(cntr[cnt]) >= min_contour_length:
            con3count_pos_in_con3.append(cnt)
            contours3_in_count.append(cntr[cnt])
    return con3count_pos_in_con3,contours3_in_count

