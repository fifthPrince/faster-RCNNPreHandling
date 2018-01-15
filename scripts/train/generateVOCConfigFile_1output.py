# -*- coding: iso-8859-15 -*-
import os
import generatexml
import cv2
from cv2 import imread

workpath = os.getenv("WORKPATH")
imagepath = os.getenv("IMAGEPATH")
imgDir = workpath + "/" + imagepath + '/img/'

destVOCImagePath = imgDir + 'VOC2012'
annotationdir = workpath + "/" + imagepath + '/img/VOC2012/Annotations'
MainDir = workpath + "/" + imagepath + '/img/VOC2012/ImageSets/Main/'

faultyName = "faulty"

#gz01:000131961_K620214_71_3_25$支持装置-套管座-螺栓$状态异常-松动.jpg:00001.jpg:支持装置-套管座-螺栓:s0001:(194, 64, 240, 88)
def generateAnnotation():
  imageDesFile = open(imgDir + "imageDescriptor","r")
  for line in imageDesFile.readlines():    
    (rPath,oldFileName,newFileName,oldObjName,newObjectName,location) = line.split(":")    
    img = imread(imgDir + "VOC2012/JPEGImages/" + newFileName)
    loc = location.strip()[1:-1]
    locList = loc.split(",")
    x0 = locList[0].strip()
    y0 = locList[1].strip()
    x1 = locList[2].strip()
    y1 = locList[3].strip()
    generatexml.generateAnnotation(faultyName,(x0,y0,x1,y1),newFileName,str(img.shape[1]),str(img.shape[0]),annotationdir)
  imageDesFile.close()


def  generateTxtInImageSetsMain():
  imageDesFile = open(imgDir + "imageDescriptor","r")
  obj2filemapDic={}
  for line in imageDesFile.readlines():    
    (rPath,oldFileName,newFileName,oldObjName,newObjectName,location) = line.split(":")    
    if obj2filemapDic.has_key(faultyName):
      obj2filemapDic[faultyName].append(newFileName[:-4])
    else:
      obj2filemapDic[faultyName]=[newFileName[:-4]]
  printdestVOCImagePathilemapDic
      
  
  path = os.path.join(desDir + "/" + "JPEGImages")
  images = os.listdir(path)
  howManyimages = len(images)
  howManyTrainImages = int(howManyimages * 0.7)
  howManyValImages = howManyimages - howManyTrainImages

  print "howManyimages is ", howManyimages

  for key,values in obj2filemapDic.items():
    objName = key
    print "objName is ", objName
    fidtrain = open(MainDir+str(objName)+"_train.txt","w")
    fidval = open(MainDir+str(objName)+"_val.txt","w")
    fidtrainval = open(MainDir+str(objName)+"_trainval.txt","w")

    
    for i in range(howManyTrainImages): #1.jpg,2.jpg, picture
      beMatched=False
      print "obj2fileMappingdic.get(key)", values
      for fileName in values:
        if(images[i][:-4] == fileName):
          beMatched = True
          print "matched", fileName

      if beMatched:
        fidtrain.write(images[i][:-4] + " " + "1" + "\n")
        fidtrainval.write(images[i][:-4] + " " + "1" + "\n")
      else:
        fidtrain.write(images[i][:-4] + " " + "-1" + "\n")
        fidtrainval.write(images[i][:-4] + " " + "-1" + "\n")

    for i in range(howManyTrainImages,howManyimages): #1.jpg,2.jpg, picture
      beMatched=False
      print "obj2fileMappingdic.get(key)", values
      for fileName in values:
        if(images[i][:-4] == fileName):
          beMatched = True
          print "matched", fileName

      if beMatched:
        fidval.write(images[i][:-4]  + " " + "1" + "\n")
        fidtrainval.write(images[i][:-4]  + " " + "1" + "\n")
      else:
        fidval.write(images[i][:-4] + " " + "-1" + "\n")
        fidtrainval.write(images[i][:-4]  + " " + "-1" + "\n")
    fidtrain.close()
    fidval.close()
    fidtrainval.close()
  imageDesFile.close()

if __name__ == '__main__':
  generateAnnotation()
  generateTxtInImageSetsMain()
