#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 11:53:27 2018

@author: siwen_chen
"""
import xlrd  
from xlutils.copy import copy  

#file = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample1-HannoNIR880603/parameter_setting_fixed.xls'
#file = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample2-HannoNIR880683/parameter_setting_fixed.xls'
file = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample3-HannoNIR880743/parameter_setting_fixed.xls'
#file = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample4-HannoNIR880613/parameter_setting_fixed.xls'
#file = '/Users/siwen_chen/Desktop/MABthesis_Siwen_Chen/results and evaluation/tracking/myResults/sample5-HannoNIR880673/parameter_setting_fixed.xls'

def writeinexcel_parameters(row, col, content):
    rb = xlrd.open_workbook(file)  
    wb = copy(rb)  
    ws = wb.get_sheet(0)  
    ws.write(row, col, content)  
    wb.save(file)  
    
    
def read_parameter(row):

    data = xlrd.open_workbook(file)
    table = table = data.sheets()[0]
    
    vector_sample_distance = table.cell(row,1).value
    value_hsv = table.cell(row,2).value
    canny_low_threshold = table.cell(row,3).value
    threshold_IOU = table.cell(row,4).value
    min_contour_length = table.cell(row,5).value
    vector_angle_low_threshold = table.cell(row,6).value
    vector_angle_high_threshold = table.cell(row,7).value
    threshold_seg_dist = table.cell(row,8).value
    
    return vector_sample_distance,value_hsv,canny_low_threshold,threshold_IOU,min_contour_length,vector_angle_low_threshold,vector_angle_high_threshold,threshold_seg_dist