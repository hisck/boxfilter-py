# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 23:25:50 2020

@author: Mateus Tenorio dos Santos & Antonio Roberto dos Santos
"""

import cv2
import numpy as np
import sys, getopt

def main(argv):
    proportion = 1
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:p:", ["ifile=", "ofile=", "pfile="])
    except getopt.GetoptError:
        print ('boxFilter.py -i <inputfile> -o <outputfile> -p <proportion>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('boxFilter.py -i <inputfile> -o <outputfile> -p <proportion>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-p", "--pfile"):
            proportion = int(arg)
            
    print ('Input file is "', inputfile)
    print ('Output file is "', outputfile)
    print ('Proportion is "', proportion)
    image = cv2.imread(inputfile, cv2.IMREAD_COLOR)
    greyscale = cv2.imread(inputfile, cv2.IMREAD_GRAYSCALE)
    cv2.imshow('Original image', image)
    cv2.imshow('Greyscale image', greyscale)
    height = image.shape[0]
    width = image.shape[1]
    
    columns = []
    lines = []
    
    i = 0
    j = 0
    
    blur = cv2.GaussianBlur(image,(5,5),0)
    
    #Matriz é percorrida para cálculo das médias
    while i < height:
        while j < width:
            media = image[i:proportion+i, j:proportion+j]
            new_pixel = int(media.mean())
            j += proportion
            columns.append(new_pixel)
        lines.append(columns)
        columns = []
        i += proportion
        j = 0
        
    #Matriz da imagem com blur é percorrida para cálculo das médias
    blur_lines = []
    blur_columns = []
    
    height_blur = blur.shape[0]
    width_blur = blur.shape[1]
    i = 0
    j = 0
    
    while i < height_blur:
        while j < width_blur:
            media = image[i:proportion+i, j:proportion+j]
            new_pixel = int(media.mean())
            j += proportion
            blur_columns.append(new_pixel)
        blur_lines.append(blur_columns)
        blur_columns = []
        i += proportion
        j = 0
        
    reduced_image = np.array(lines, dtype = np.uint64)
    #print('New resolution for image is : %d pixels height and %d pixels width' % (reduced_image.shape[0]) %(reduced_image.shape[1]))
    reduced_blur_image = np.array(blur_lines, dtype = np.uint64)
    #print('New resolution for image is : %d pixels height and %d pixels width' % (reduced_blur_image.shape[0]) %(reduced_blur_image.shape[1]))

    #box filter downsampling
    cv2.imshow("Reduced image with box filter", reduced_image)
    cv2.imwrite(outputfile, reduced_image)
    cv2.imshow("Reduced blurred image with box filter", reduced_blur_image)
    cv2.imwrite('reduced_blurred_image.jpg', reduced_blur_image)

    #slicing downsampling
    downsampling = image[::proportion, ::proportion]
    blurred_downsampling = blur[::proportion, ::proportion]
    
    cv2.imshow("Reduced image using slicing", downsampling)
    cv2.imwrite('downsampling.jpg', downsampling)
    cv2.imshow("Reduced blurred image using slicing", blurred_downsampling)
    cv2.imwrite('blurred_downsampling.jpg', blurred_downsampling)

if __name__ == "__main__":
   main(sys.argv[1:])