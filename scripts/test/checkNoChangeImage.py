# -*- coding: iso-8859-15 -*-
import os
import cv2

imgDir = '/home/hone/miniconda2/lib/python2.7/site-packages/tensorflow/models/research/eguanwu_tielu2/img/'
originalImagePath = imgDir + 'originalimg/'



def getAllFiles(originalImagePath):
  allFileAndObjectList =[]
  gzxxDirs = os.listdir(originalImagePath)  #all directory is gzxx pattern
  gzxxDirs.sort()
  print "gzxxDirs is len", len(gzxxDirs)
  for aGzxxDir in gzxxDirs:
    fileListInGzxxDir = os.listdir(originalImagePath + aGzxxDir)
    for aFile in fileListInGzxxDir:
      #file name example: 000131961_K620214_71_3_25$支持装置-套管座-螺栓$状态异常-松动.jpg
      strList = aFile[:-4].split("$") #-4 means "remove .jgp" and then split with $
      if len(strList)==3: #means find the correct file. 
        allFileAndObjectList.append((aFile,strList[1],aGzxxDir))
        shortFileName = strList[0] + ".jpg"
        
        longFile = cv2.imread(originalImagePath + aGzxxDir + "/" + aFile)
        shortFile = cv2.imread(originalImagePath + aGzxxDir + "/" +  shortFileName)
        print " longfile shape is "+ str(longFile.shape) + ":" + str(shortFile.shape)
        if(longFile.shape != shortFile.shape):
          print "wrong with " + aFile + " in " + aGzxxDir
      elif (len((strList)))>0 and (aFile.find("$")!=-1):
        print "exception ",aFile

      
   
  return  allFileAndObjectList

getAllFiles(originalImagePath)
