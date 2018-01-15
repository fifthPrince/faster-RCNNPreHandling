# -*- coding: iso-8859-15 -*-

#not good effect using original image. so crop the image so taht it only contains the marked part.
import os
import sys
from cv2 import imread,imwrite
import restore_annotation
import random

##############################
#change following configurations based your own environment
##############################
#Point to your own source image files
workpath = os.getenv("WORKPATH")
imagepath = os.getenv("IMAGEPATH")
originalImagePath = workpath + 'try/'

imgDir = workpath + "/" + imagepath + '/img/'
destVOCImagePath = imgDir + 'VOC2012'
if os.path.exists(imgDir) == False:
  os.mkdir(imgDir)
mapFile = open(imgDir + "fromsrc2desImages.map","w")
cpCmdRecordFile = open(workpath + '/scripts/tmp/cpCmdRecordFile','w')

def getAllFiles(originalImagePath):
  allFileAndObjectList =[]
  gzxxDirs = os.listdir(originalImagePath)  #all directory is gzxx pattern
  gzxxDirs.sort()
  print "gzxxDirs is len", len(gzxxDirs)
  for aGzxxDir in gzxxDirs:
    fileListInGzxxDir = os.listdir(originalImagePath + aGzxxDir)
    for aFile in fileListInGzxxDir:
      #file name example: 000131961_K620214_71_3_25$æ¯æè£çœ®-å¥ç®¡åº§-èºæ $ç¶æåŒåžž-æŸåš.jpg
      strList = aFile[:-4].split("$") #-4 means "remove .jgp" and then split with $
      if len(strList)==3: #means find the correct file. 
        allFileAndObjectList.append((aFile,strList[1],aGzxxDir))
      elif (len((strList)))>0 and (aFile.find("$")!=-1):
        print "exception ",aFile
   
  return  allFileAndObjectList
##############################################
#end for your change
##############################################

def printList(lst):
  for l in lst:
    print l

def renameFile(oldFileName,i):
  return "0000" + str(i) + ".jpg"

def copyToDestination(relativePath,oldFile,newFile,destVOCImagePath):
  dollorIndex = oldFile.find("$")
  shortFileName = oldFile[:dollorIndex] + ".jpg"
  cmd = 'cp ' + '\'' +originalImagePath  + relativePath + '/' +shortFileName + '\'' + ' ' + destVOCImagePath + '/JPEGImages/'+ newFile  
  os.system(cmd)
  cmd = 'cp ' + '\'' +originalImagePath  + relativePath + '/' +oldFile + '\'' + ' ' + destVOCImagePath + '/JPEGImagesMark/'+ newFile
  cpCmdRecordFile.write(cmd + " \n")
  os.system(cmd)

def recordTheNewFileName(relativePath,oldFile,newFile,objectName):
  mapFile.write(relativePath + ":" + oldFile + ":" + newFile + ":" + objectName + "\n")

def generateVOCJPEGImages():
  tupleList = getAllFiles(originalImagePath)  # tuple (filename,objectname,directory)
 
  #handle image one by one
  i = 1
  for aFileTuple in tupleList:    
    newFileName = renameFile(aFileTuple[0],i)     
    copyToDestination(aFileTuple[2],aFileTuple[0],newFileName,destVOCImagePath)
    recordTheNewFileName(aFileTuple[2],aFileTuple[0],newFileName,aFileTuple[1])
    i+=1
    

  mapFile.close()
  checkAllFileOK(len(tupleList))

def generateVOCDir():

  if os.path.exists(destVOCImagePath) == False:
    os.mkdir(destVOCImagePath)
  path=os.chdir(destVOCImagePath)
  if os.path.exists('JPEGImages') == False:
    os.mkdir('JPEGImages')
  if os.path.exists('JPEGImagesMark') == False:
    os.mkdir('JPEGImagesMark')
  if os.path.exists('Annotations') == False:
    os.mkdir('Annotations')
  if os.path.exists('ImageSets') == False:
    os.mkdir('ImageSets')
    os.mkdir('ImageSets/Main')

def checkAllFileOK(length):
  print "checkAllFileOK length is ", length
  fileNumberDic = {}
  fileList = os.listdir(destVOCImagePath+'/JPEGImages')
  for aFile in fileList:
    fileNumberDic[int(aFile[:-4])]=1

  broken=False
  for i in range(1,length+1):
    if fileNumberDic.has_key(i):
      #print str(i) + " is OK"
      pass
    else:
      print str(i) + " is missing"
      broken = True

  if broken:
    sys.exit()

#original image is too big. it can not run in faster rcnn at least in my computer.
#4400*6600 is a typcal example. resize to 440*660.
#refer to http://blog.csdn.net/Best_Coder/article/details/76577544?locationNum=8&fps=1
#è¿äºåŸåçåçŽ å°ºå¯žå€§å°äžäžïŒäœæ¯æšªååŸçå°ºå¯žå€§çºŠåš500*375å·Šå³ïŒçºµååŸçå°ºå¯žå€§çºŠåš375*500å·Šå³ïŒ
#åºæ¬äžäŒåå·®è¶è¿100ãïŒåšä¹åçè®­ç»äž­ïŒç¬¬äžæ­¥å°±æ¯å°è¿äºåŸçéœresizeå°300*300ææ¯500*500ïŒææåå§åŸçäžèœçŠ»è¿äžªæ åè¿è¿ã
def resizeAllTheImages():
  path = os.path.join(destVOCImagePath + "/" + "JPEGImagesMark")
  images = os.listdir(path)
  for aFile in images:
    print "file is ", aFile
    img= imread(os.path.join(path,aFile))
    (x0,y0,x1,y1) = restore_annotation.getObjectLocation(img)
    print "(x0,y0,x1,y1) is ", (x0,y0,x1,y1)
    markHeight = y1 - y0
    markWeidht = x1 - x0
    ran1 = 3*random.random()
    ran2 = 4*random.random()
    ran3 = 4.5*random.random()
    ran4 = 5*random.random()
    print "ran1 ran1 ran1 ran1" , (ran1,ran2,ran3,ran4)
    realx0=x0 - int(markWeidht*ran1) if x0 - int(markWeidht*ran1) > 0 else 0
    realy0=y0 - int(markHeight*ran2) if y0 - int(markHeight*ran2) > 0 else 0
    realx1=x1 + (int(markWeidht*ran3)) if x1 + (int(markWeidht*ran3)) < img.shape[1] else img.shape[1]
    realy1=y1 + (int(markHeight*ran4)) if y1 + (int(markHeight*ran4)) < img.shape[0] else img.shape[0]
    print "(realx0,realy0,realx1,realy1) is " , (realx0,realy0,realx1,realy1)
    patch_tree = img[realy0:realy1,realx0:realx1]
    imwrite(os.path.join(path,aFile),patch_tree)
    
    img2 = imread(os.path.join(destVOCImagePath + "/" + "JPEGImages",aFile))
    patch_tree2 = img2[realy0:realy1,realx0:realx1]
    imwrite(os.path.join(destVOCImagePath + "/" + "JPEGImages",aFile),patch_tree2)

  print "resizeAllTheImagesMark is done"
  

if __name__ == '__main__':
  generateVOCDir()
  generateVOCJPEGImages()
  resizeAllTheImages()  
  os.system('cp ' + imgDir + "fromsrc2desImages.map " + imgDir + "fromsrc2desImages.map.backup")

