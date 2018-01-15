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
    
    
def generateNinePieces(width, height):
    print "width/3,height/3, height/3,2*width/3,2*height/3", (width/3,height/3,2*width/3,2*height/3)
    return[(0,0,width/3,height/3),(width/3,0,2*width/3,height/3),(2*width/3,0,width,height/3),
           (0,height/3,width/3,2*height/3),(width/3,height/3,2*width/3,2*height/3),(2*width/3,height/3,width,2*height/3),
           (0,2*height/3,width/3,height),(width/3,2*height/3,2*width/3,height),(2*width/3,2*height/3,width,height)]
    

def generateNewImagesPiece(piece,img,aFile,i):
    imagepiece = img[piece[1]:piece[3],piece[0]:piece[2]]
    imwrite(aFile[:-4] + "_" + str(i) + ".jpg",imagepiece)

def if_intersection(xmin_a, xmax_a, ymin_a, ymax_a, xmin_b, xmax_b, ymin_b, ymax_b):
    if_intersect = False
  
    if xmin_a < xmax_b <= xmax_a and (ymin_a < ymax_b <= ymax_a or ymin_a <= ymin_b < ymax_a):
        if_intersect = True
    elif xmin_a <= xmin_b < xmax_a and (ymin_a < ymax_b <= ymax_a or ymin_a <= ymin_b < ymax_a):
        if_intersect = True
    elif xmin_b < xmax_a <= xmax_b and (ymin_b < ymax_a <= ymax_b or ymin_b <= ymin_a < ymax_b):
        if_intersect = True
    elif xmin_b <= xmin_a < xmax_b and (ymin_b < ymax_a <= ymax_b or ymin_b <= ymin_a < ymax_b):
        if_intersect = True
    else:
        return False

    if if_intersect == True:
        x_sorted_list = sorted([xmin_a, xmax_a, xmin_b, xmax_b])
        y_sorted_list = sorted([ymin_a, ymax_a, ymin_b, ymax_b])
        x_intersect_w = x_sorted_list[2] - x_sorted_list[1]
        y_intersect_h = y_sorted_list[2] - y_sorted_list[1]
        area_inter = x_intersect_w * y_intersect_h
        return (x_sorted_list[1],y_sorted_list[1],x_sorted_list[2],y_sorted_list[2])
    
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
    imageHeight = img.shape[0]
    imageWidth = img.shape[1]
    print "(imageHeight,imageWidth) is ", (imageHeight,imageWidth)
    ninePieces = generateNinePieces(imageWidth,imageHeight)
    i = 0
    for piece in ninePieces:
        print "piece[0],piece[1],piece[2],piece[3] is ", (piece[0],piece[1],piece[2],piece[3]) 
        area = if_intersection(piece[0],piece[2],piece[1],piece[3],x0,x1,y0,y1)
        i = i + 1
        if(area != False):
          print "generate image for i", i
          generateNewImagesPiece(piece,img,aFile,i)
        else:
          continue     
    

  print "resizeAllTheImagesMark is done"
  

if __name__ == '__main__':
  generateVOCDir()
  generateVOCJPEGImages()
  resizeAllTheImages()  
  os.system('cp ' + imgDir + "fromsrc2desImages.map " + imgDir + "fromsrc2desImages.map.backup")

