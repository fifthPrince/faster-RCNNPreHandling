
import os
import generatexml
import cv2
from cv2 import imread

originalImagePath = "/root/work/img/originalimg/"

destVOCImagePath = "/root/work/img/VOC2012/JPEGImages/"

def generateAnnotation():
  imageDesFile = open("/root/work/img/imageDescriptor","r")
  os.chdir(destVOCImagePath)
  for line in imageDesFile.readlines():    
    (rPath,oldFileName,newFileName,oldObjName,newObjectName,location) = line.split(":") 
    if os.path.exists(newObjectName) == False:
        os.mkdir(newObjectName)
    if newObjectName == "s00012":
      cmd = "cp " + originalImagePath + "/" + rPath + "/" + oldFileName + " " + destVOCImagePath + "/" + newFileName
      print cmd
      os.system("cp " + originalImagePath + "/" + rPath + "/" + oldFileName + " " + destVOCImagePath + "/" + newObjectName + "/" + newFileName)
if __name__ == '__main__':
    generateAnnotation()
    pass
