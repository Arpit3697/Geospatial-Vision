# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 23:38:54 2020

@author: harih
"""

import cv2
import numpy as np
import os

#Change path according to where your data is
path = "C:/Masters/university/GeoVV/HW1/sample_drive"

def start_detection(dir_path):
   
    directories = os.listdir(dir_path)
    dir_list = []
    for d in directories:
        dir_list.append(d)
    for directory in dir_list:
        temp_path = path + '/' + directory
        data_set = process_image(temp_path)
        final_data_set = split_data(data_set)

        print ('Mean Image', directory)
        mean_img = create_mean_image(final_data_set)
        cv2.imwrite(directory + '_mean_image.jpg',mean_img)
        
        print ('Smoothended Image', directory)
        prelim_mask = create_prelim_mask(mean_img.astype('uint8'))
        cv2.imwrite(directory + '_smoothened_image.jpg',prelim_mask)
        
        print ('Final Mask', directory)
        final_image = create_binary_mask(prelim_mask)
        cv2.imwrite(directory + '_final_mask.jpg',final_image)
    


def process_image(dir_path):
  
    images = []
    for image in os.listdir(dir_path):
        img = cv2.imread(os.path.join(dir_path,image))
        if img is not None:
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eq_img = cv2.equalizeHist(gray_image)
            blur_img = cv2.blur(eq_img, (3,3))
            ret,thresh_img = cv2.threshold(blur_img,127,255,cv2.THRESH_BINARY)
            images.append(thresh_img)
    return images
        

def split_data(image_set):
 
    total = []
    count = 0
    number_of_splits = len(image_set)/200
    for i in range(int(number_of_splits)):
        maxcount = count + 200
        if maxcount < len(image_set)-1:
            temp_arr = image_set[count:maxcount]
        else:
            temp_arr = image_set[count:]
        total.append(temp_arr)
        count += 200
    return total


def calc_mean_image(arr, length):

    i = 1
    sum_image = arr[0] * 1/length
    while (i < len(arr)):
        sum_image = cv2.add(sum_image,arr[i]* 1/length)
        i += 1
    return sum_image


def create_mean_image(total_data):
  
    avg_images = []
    for data in total_data:
        temp_img = calc_mean_image(data,len(data))
        avg_images.append(temp_img)
    
    return calc_mean_image(avg_images,len(avg_images))
    

def create_prelim_mask(img):
   
    adapt = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,105,11)
    return cv2.bitwise_not(adapt)
    

def create_binary_mask(img):
  
    kernel = np.ones((10,10),np.uint8)
    erosion = cv2.erode(img,kernel,iterations = 5)
    dilation = cv2.dilate(erosion,kernel,iterations = 5)
    return dilation

start_detection(path)