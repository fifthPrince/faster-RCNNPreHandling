import os
import cv2
from cv2 import imread
import restore_annotation
import generatexml


workpath = os.getenv("WORKPATH")
imagepath = os.getenv("IMAGEPATH")
imgDir = workpath + "/" + imagepath + '/img/'

originalImagePath = workpath + 'originalimg/'
destVOCImagePath = imgDir + 'VOC2012'

imageDesFile = open(imgDir + "imageDescriptor","w")

annotationdir = workpath + "/" + imagepath + '/img/VOC2012/Annotations'

ObjectMappingDic = {}

def generateBoxes():  
  imgLocationDic={}
  path = os.path.join(destVOCImagePath + "/" + "JPEGImagesMark")
  images = os.listdir(path)
  for aFile in images:
    img = imread(os.path.join(path,aFile))
    location = restore_annotation.getObjectLocation(img)
    imgLocationDic[aFile]=(location,str(img.shape[0]),str(img.shape[1]))
  return imgLocationDic

#from file fromsrc2desImages.map get (relativePath + " " + oldFile + " " + newFile + " " + objectName)
def generateFileMeta(imgLocationDic):
  mapFile = open(imgDir + "fromsrc2desImages.map","r")
  for line in mapFile.readlines():
    #print line
    (rPath,oldFileName,newFileName,oldObjName) = line.split(":")
    #print (rPath,oldFileName,newFileName,objName)
    imageDesFile.write(line.strip() + ":" + ObjectMappingDic[oldObjName] + ":" + str(imgLocationDic[newFileName][0]) + "\n")
  mapFile.close()
  imageDesFile.close()

  
def renameObjectName():
  mapFile = open(imgDir + "fromsrc2desImages.map","r")
  counter = 1
  for line in mapFile.readlines():
    (rPath,oldFileName,newFileName,oldObjName) = line.split(":")
    if ObjectMappingDic.has_key(oldObjName):
      pass
    else:
      ObjectMappingDic[oldObjName] = "s000" + str(counter)
      counter+=1

  for key,value in ObjectMappingDic.items():
    print "key is ",key
    print "value is ", value
  mapFile.close()

if __name__ == '__main__':
  renameObjectName()
  imgLocationDic = generateBoxes()
  generateFileMeta(imgLocationDic)  
  os.system('cp ' + imgDir + "imageDescriptor " + imgDir + "imageDescriptor.backup")
  
