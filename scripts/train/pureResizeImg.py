# -*- coding: iso-8859-15 -*-
'''
Created on 2018年1月10日

@author: hone
'''
path = "/home/hone/work/ai/tieluProject/correctImg/K605782_11"
des = "/home/hone/work/ai/tieluProject/correctImg/destination"
import os
from PIL import Image

def resizeAllTheImages():
  images = os.listdir(path)
  for aFile in images:
    img=Image.open(os.path.join(path,aFile))
    out = img.resize((img.size[0]/5,img.size[1]/5))
    out.save(os.path.join(des,aFile))
  print "resizeAllTheImages is done"
  


resizeAllTheImages()