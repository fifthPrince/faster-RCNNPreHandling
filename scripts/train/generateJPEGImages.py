# -*- coding: iso-8859-15 -*-


import os
import sys
from PIL import Image

##############################
#change following configurations based your own environment
##############################
#Point to your own source image files
workpath = os.getenv("WORKPATH")
imagepath = os.getenv("IMAGEPATH")

originalImagePath = workpath + '/originalimg/'
destVOCImagePath = imagepath + '/img/VOC2012/'
tmpPath = imagepath + '/tmp/'

mapFile = open(tmpPath + "/fromOrig2VocImages.map","w")
cpCmdRecordFile = open(tmpPath + '/cpCmdRecordFile','w')

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
  path = os.path.join(destVOCImagePath + "/" + "JPEGImages")
  images = os.listdir(path)
  for aFile in images:
    img=Image.open(os.path.join(path,aFile))
    out = img.resize((img.size[0]/5,img.size[1]/5))
    out.save(os.path.join(path,aFile))
  print "resizeAllTheImages is done"

def resizeAllTheImagesMark():
  path = os.path.join(destVOCImagePath + "/" + "JPEGImagesMark")
  images = os.listdir(path)
  for aFile in images:
    img=Image.open(os.path.join(path,aFile))
    out = img.resize((img.size[0]/5,img.size[1]/5))
    out.save(os.path.join(path,aFile))

  print "resizeAllTheImagesMark is done"




if __name__ == '__main__':
  generateVOCDir()
  generateVOCJPEGImages()
  resizeAllTheImages()
  resizeAllTheImagesMark()
  os.system('cp ' + imgDir + "fromsrc2desImages.map " + imgDir + "fromsrc2desImages.map.backup")

