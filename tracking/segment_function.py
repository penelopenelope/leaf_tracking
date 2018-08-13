#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 07:26:09 2018

@author: siwen_chen
"""

def leaf_segment(path,vec_sample_dist,value_hsv,canny_low_threshold,threshold_IOU,min_contour_length,vector_angle_low_threshold,vector_angle_high_threshold,threshold_seg_dist):
    
    import cv2
    import numpy as np
    from random import randint
    from skimage import morphology
    
    import find_tips2
    import search_new_seg
    import dist_betw2segs
    import cal_IOU
    import order
    import lsf_circlefit

    img = cv2.imread(path)
    height,width,channels = img.shape
    
    # =============================================================================
    # image pre-processing
    # =============================================================================
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
    mask_plant = np.logical_and(img_hsv[:,:,0] == 0,img_hsv[:,:,2]>value_hsv)
    
    kernel = np.ones((3,3),np.uint8)     
    mask_plant = mask_plant.astype(np.uint8)   
    mask_plant = cv2.morphologyEx(mask_plant,cv2.MORPH_OPEN,kernel) 
    mask_plant = cv2.morphologyEx(mask_plant,cv2.MORPH_CLOSE,kernel) 
    
    im2, contours_0, hierarchy = cv2.findContours(mask_plant,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    areas = []
    for cntrs in contours_0:
        a = cv2.contourArea(cntrs)
        areas.append(a)
    max_cntr = contours_0[areas.index(max(areas))]
    mask_plant_bool = np.zeros((height,width),np.uint8)
    mask_plant_bool = np.logical_or(mask_plant > 0, mask_plant_bool)
    mask_plant_bool = morphology.remove_small_objects(mask_plant_bool,min_size=max(areas),connectivity=1)
    
    inner_hierarchy_contour = []
    for hierarchy_1 in hierarchy[0]:
        if hierarchy_1[2] != -1:
            inner_hierarchy_position = hierarchy_1[2]
            inner_hierarchy_contour = contours_0[inner_hierarchy_position]
    
    mask_contour = np.zeros((height,width),np.uint8)
    cv2.drawContours(mask_contour,max_cntr,-1,1,1)
    if len(inner_hierarchy_contour) != 0:
        cv2.drawContours(mask_contour,inner_hierarchy_contour,-1,1,1)
    
    gray = cv2.cvtColor(img_hsv,cv2.COLOR_BGR2GRAY)
    high_threshold = 3*canny_low_threshold
    canny_all = cv2.Canny(gray,canny_low_threshold,high_threshold)
    
    mask_plant_int = np.zeros((height,width),np.uint8)
    mask_plant_int[mask_plant_bool] = [1]
    kernel_erosion = np.ones((5,5),np.uint8)
    mask_plant_erosion = cv2.erode(mask_plant_int,kernel_erosion,iterations = 4)
    
    inner_contours_bool = np.logical_and(mask_plant_erosion > 0, canny_all > 0)
    inner_contours_int = np.zeros((height,width),np.uint8)
    inner_contours_int[inner_contours_bool] = [1]
    
    kernel_cnt_neighbors = np.array([[1,1,1],
                                    [1,0,1],
                                    [1,1,1]],dtype = np.uint8)  
    neighbors_count = cv2.filter2D(mask_contour,-1,kernel_cnt_neighbors)  
    mask_junction = np.logical_and(neighbors_count >= 3, mask_contour>0)
    mask_contour[mask_junction] = [0]           

    kernel_dilate = np.ones((3,3),np.uint8)
    inner_contours_dilate = cv2.morphologyEx(inner_contours_int, cv2.MORPH_CLOSE, kernel_dilate)  
    
    inner_contours = np.zeros((height,width),np.uint8)
    inner_contours = np.logical_or(inner_contours_dilate > 0,inner_contours)
    mask_contour[inner_contours] = [1]
    
    im3,contours2,hierarchy2 = cv2.findContours(mask_contour,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)    
    img_show2 = img.copy()
    for c in contours2:
        cv2.drawContours(img_show2,[c],0,(randint(0,255),randint(0,255),randint(0,255)),2)  

    def angle_vec(v1,v2):
        v1_norm = v1 / np.linalg.norm(v1)
        v2_norm = v2 / np.linalg.norm(v2)
        cos_vec = np.dot(v1_norm,v2_norm)
        cos_vec = np.clip(cos_vec,-1.0,1.0)       
        angle = np.arccos(cos_vec)*180/np.pi
        return angle
    
    img_show4 = img.copy()
    for a in contours2:
        cv2.drawContours(img_show4,[a],0,(255,255,0),1)
    
    mask_contour_after_cut = mask_contour.copy()
    
    i = 0
    for cnt in contours2:      
        for j in range(vec_sample_dist,len(cnt) - vec_sample_dist):  
                vec1 = cnt[j] - cnt[j - vec_sample_dist]
                vec2 = cnt[j + vec_sample_dist] - cnt[j]
                vector_angle = angle_vec(vec1[0],vec2[0])
                if vector_angle >= vector_angle_low_threshold and vector_angle <= vector_angle_high_threshold:             #angle threshold
                    seg = [
                           cnt[j]
    #                       cnt[j+1]
                           ]
                    cv2.drawContours(img_show4,seg,0,(255,0,0),2)
                    cv2.drawContours(mask_contour_after_cut,seg,0,[0],2)
                    if seg[0][0][0] >= len(mask_contour) or seg[0][0][1] >= len(mask_contour):
                        continue
                    mask_contour[seg] = [0]
        i = i + 1
        if i >= len(contours2):
            break
            
    im4,contours3,hierarchy3 = cv2.findContours(mask_contour_after_cut,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)     
    img_show5 = img.copy()
    for c in contours3:
        cv2.drawContours(img_show5,[c],0,(randint(0,255),randint(0,255),randint(0,255)),2)  

    con3count_pos_in_con3,contours3_in_count = search_new_seg.con3_incount(contours3,min_contour_length)
    
    img_show6 = img.copy()  
    
    i = 0;
    for i in range(0,len(contours3_in_count)):
        
        cnt = contours3_in_count[i]
        if(len(cnt) <= min_contour_length):
            continue;
        col = (randint(0,255),randint(0,255),randint(0,255))
        
        x_centr,y_centr,radius = lsf_circlefit.lsf_circle(cnt)
        cv2.circle(img_show6,(int(x_centr),int(y_centr)),int(radius),col,2)
        cv2.drawContours(img_show6,[cnt],0,col,2)
        cv2.putText(img_show6,str(i),(int(x_centr),int(y_centr)),1,2,col,1,cv2.LINE_AA)    
    
    new_seg_to_descend = []
    for tnt in range(len(contours3_in_count)-1):
        tips_fixed = find_tips2.find_tips(contours3_in_count[tnt])
             
        if len(tips_fixed) != 2:       
            continue
                                            
        fixed_seg_img, __ = cal_IOU.circle_img(path,contours3_in_count[tnt])
        IOUandpos_list_for_fixed_seg = []
        for ttnt in range(tnt + 1, len(contours3_in_count)):
            tips_test = find_tips2.find_tips(contours3_in_count[ttnt])
            
            if len(tips_test) != 2:
                continue
                            
            dist,new_tip1,new_tip2 = dist_betw2segs.dist_between_two_segs(tips_fixed,tips_test)
            if dist <= threshold_seg_dist:
                IOU = cal_IOU.cal_IOU(path,fixed_seg_img,contours3_in_count[ttnt])
                IOU_and_pos = (IOU,ttnt)
                IOUandpos_list_for_fixed_seg.append(IOU_and_pos)
                if IOU >= threshold_IOU:
                    segs_to_combine = (IOU,tnt,ttnt)
                    new_seg_to_descend.append(segs_to_combine)
        IOU_descending_list_perseg = order.descending_order(IOUandpos_list_for_fixed_seg)
        if IOU_descending_list_perseg == []:
            continue
        
    new_seg_descended = order.descending_order(new_seg_to_descend)    
     
    to_combine_seg_list = []
    for fnt in range(len(new_seg_descended)):
        ffnt = [new_seg_descended[fnt][1],new_seg_descended[fnt][2]]
        to_combine_seg_list.append(ffnt)
    
    if len(to_combine_seg_list) == 0:
        new_seg_list = []
    else:
        new_seg_list = [to_combine_seg_list[0]]
        for gnt in range(1,len(to_combine_seg_list)):
            seg_pair = to_combine_seg_list[gnt]
            seg_pair_grouped_ornot = False
            seg_pair_img = cal_IOU.shape(path,contours3_in_count,seg_pair)
            
            for hnt in range(len(new_seg_list)):
                if hnt >= len(new_seg_list):
                    break
                new_seg_group = new_seg_list[hnt]
                new_seg_group_shape_img = cal_IOU.shape(path,contours3_in_count,new_seg_group)
                
                for new_seg_group_member in new_seg_group:
                    
                    
                    
                    if seg_pair[0] == new_seg_group_member:
                        the_other_seg_already_grouped_ornot = False
                        for pnt in range(len(new_seg_list)):
                            new_seg_group2 = new_seg_list[pnt]
                            for new_seg_group_member2 in new_seg_group2:
                                if seg_pair_grouped_ornot == True:
                                    break
                                
                                if new_seg_group_member2 == seg_pair[1]:
                                    the_other_seg_already_grouped_ornot = True
                                    new_seg_group2_shape_img = cal_IOU.shape(path,contours3_in_count,new_seg_group2)
                                    new_IOU = cal_IOU.cal_IOU1(new_seg_group_shape_img,new_seg_group2_shape_img)
                                    if new_IOU >= threshold_IOU:
                                        updated_seg_group = new_seg_group2 + new_seg_group
                                        new_seg_list[hnt] = updated_seg_group
                                        del new_seg_list[pnt]
                                        seg_pair_grouped_ornot = True
                                if the_other_seg_already_grouped_ornot == False:
                                    new_IOU = cal_IOU.cal_IOU1(seg_pair_img,new_seg_group_shape_img)
                                    if new_IOU >= threshold_IOU:
                                        new_seg_group.append(seg_pair[1])
                                        seg_pair_grouped_ornot = True                            
                                    break
                                break
                            break
                        break
                    
                    if seg_pair[1] == new_seg_group_member:
                        the_other_seg_already_grouped_ornot = False
                        
                        
                        
                        for pnt in range(len(new_seg_list)):
                            new_seg_group3 = new_seg_list[pnt]
                            for new_seg_group_member3 in new_seg_group3:
                                if seg_pair_grouped_ornot == True:
                                    break
                                
                                
                                if new_seg_group_member3 == seg_pair[0]:
                                    the_other_seg_already_grouped_ornot = True
                                    new_seg_group3_shape_img = cal_IOU.shape(path,contours3_in_count,new_seg_group3)
                                    new_IOU = cal_IOU.cal_IOU1(new_seg_group_shape_img,new_seg_group3_shape_img)
                                    if new_IOU >= threshold_IOU:
                                        updated_seg_group = new_seg_group3 + new_seg_group
                                        new_seg_list[hnt] = updated_seg_group
                                        del new_seg_list[pnt]
                                        seg_pair_grouped_ornot = True
                                if the_other_seg_already_grouped_ornot == False:
                                    new_IOU = cal_IOU.cal_IOU1(seg_pair_img,new_seg_group_shape_img)
                                    if new_IOU >= threshold_IOU:
                                        new_seg_group.append(seg_pair[0])
                                        seg_pair_grouped_ornot = True
                                
                                    break
                                break
                            break
                        break
                                    
            if seg_pair_grouped_ornot == False:
                new_seg_list.append(seg_pair)
    
    #to avoid merging mistake
    new_seg_list_2 = []
    for segs in new_seg_list:
        uniq_segs = np.unique(segs)
        new_seg_list_2.append(list(uniq_segs))
    new_seg_list_3 = order.find_finalcomb(new_seg_list_2)    
    
    img_show7 = img.copy()
    for jnt in new_seg_list_3:
        if new_seg_list_3 == []:
            break
        color = randint(0,255),randint(0,255),randint(0,255)
        for jjnt in jnt:
            cv2.drawContours(img_show7,[contours3_in_count[jjnt]],0,color,2)
    
    uniq_seg_list = []
    for lnt in new_seg_list_3:
        if new_seg_list_3 == []:
            break
        uniq_seg_list.extend(lnt)    
    
    contours3_in_count_list = []
    for lnt in range(len(contours3_in_count)):
        contours3_in_count_list.append(lnt)
    left_single_segs = [mnt for mnt in contours3_in_count_list if mnt not in uniq_seg_list]
    for nnt in left_single_segs:
        nnnt = contours3_in_count[i]
        if(len(nnnt) <= min_contour_length):
            continue;
        
        col3 = (randint(0,255),randint(0,255),randint(0,255))
        cv2.drawContours(img_show7,contours3_in_count[nnt],-1,col3,2)
    #    final_seg.append(nnt)

# =============================================================================
# for check
# =============================================================================
    from matplotlib import pyplot as plt

    plt.imshow(img_show7)
    plt.show()

# =============================================================================
# 
# =============================================================================
    comb_part = []
    for ont in new_seg_list_3:
        contour = []
        for oont in ont:
            contour.append(contours3_in_count[oont])
        comb_part.append(contour)
#    print(len(comb_part))
    
    for sing in left_single_segs:
        sing_cnt = contours3_in_count[i]
        if(len(sing_cnt) <= min_contour_length):
            continue;

        contour1 = []
        contour1.append(contours3_in_count[sing])
        comb_part.append(contour1)
    
    contours4 = comb_part
    
    return contours4
