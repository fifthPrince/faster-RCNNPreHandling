# -*- coding: iso-8859-15 -*-
from cv2 import imread

import cv2
import numpy as np

def getObjectLocation(img):
    
  img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  # lower mask (0-10)
  lower_red = np.array([0,50,50])
  upper_red = np.array([10,255,255])
  mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

  # upper mask (170-180)
  lower_red = np.array([170,50,50])
  upper_red = np.array([180,255,255])
  mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

  # join my masks
  mask = mask0+mask1

  # set my output img to zero everywhere except my mask
  output_img = img.copy()
  output_img[np.where(mask==0)] = 0
  output_img[np.where(mask!=0)] = 255

  img = output_img

  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
  contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  cnt=contours[0]
  for item in contours[1:]:  
    cnt = np.concatenate((cnt,item),axis=0)
   
  x,y,w,h = cv2.boundingRect(cnt)
  print "before return x,y,w,z"
  print x,y,w,h
  return x,y,x+w,y+h

if __name__ == "__main__":
    img = imread("00002_4.jpg")
    getObjectLocation(img)

# screen_res = 1280, 720
# scale_width = screen_res[0] / img.shape[1]
# scale_height = screen_res[1] / img.shape[0]
# scale = min(scale_width, scale_height)
# window_width = int(img.shape[1] * scale)
# window_height = int(img.shape[0] * scale)
#
# cv2.namedWindow('dst_rt', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('dst_rt', window_width, window_height)
#
# cv2.imshow('dst_rt', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
