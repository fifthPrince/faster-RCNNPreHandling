# -*- coding: utf-8 -*-


import os
import sys
from PIL import Image

##############################
#change following configurations based your own environment
##############################
#Point to your own source image files
workpath = os.getenv("WORKPATH")
imagepath = os.getenv("IMAGEPATH")
originalImagePath = workpath + 'originalimg/'

imgDir = workpath + "/" + imagepath + '/img/'
destVOCImagePath = imgDir + 'VOC2012'
mapFile = open(imgDir + "fromsrc2desImagess00012.map","w")
cpCmdRecordFile = open(workpath + '/scripts/tmp/cpCmdRecordFile','w')

def getAllFiles(originalImagePath):
  allFileAndObjectList =[]
  gzxxDirs = os.listdir(originalImagePath)  #all directory is gzxx pattern
  gzxxDirs.sort()
  print "gzxxDirs is len", len(gzxxDirs)
  for aGzxxDir in gzxxDirs:
    fileListInGzxxDir = os.listdir(originalImagePath + aGzxxDir)
    for aFile in fileListInGzxxDir:
      #file name example: 000131961_K620214_71_3_25$ÃŠÂÂ¯ÃŠÂÂÃšÂ£ÂÃ§ÅÂ®-Ã¥Â¥ÂÃ§Â®Â¡Ã¥ÂºÂ§-ÃšÂÂºÃŠÂ Â$Ã§ÂÂ¶ÃŠÂÂÃ¥ÅÂÃ¥ÅŸÅŸ-ÃŠÂÅžÃ¥ÂÅ¡.jpg
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
    if aFileTuple[1] == "接触悬挂":
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
#ÃšÂ¿ÂÃ€ÂºÂÃ¥ÂÅžÃ¥ÂÂÃ§ÂÂÃ¥ÂÂÃ§ÅœÂ Ã¥Â°ÂºÃ¥Â¯ÅŸÃ¥â¬Â§Ã¥Â°ÂÃ€ÅŸÂÃ€ÅŸÂÃ¯ÅÂÃ€ÅÂÃŠÂÂ¯ÃŠÅ¡ÂªÃ¥ÂÂÃ¥ÂÅžÃ§ÂÂÃ¥Â°ÂºÃ¥Â¯ÅŸÃ¥â¬Â§Ã§ÂºÅ Ã¥ÂÅ¡500*375Ã¥Â·Å Ã¥ÂÂ³Ã¯ÅÂÃ§ÂºÂµÃ¥ÂÂÃ¥ÂÅžÃ§ÂÂÃ¥Â°ÂºÃ¥Â¯ÅŸÃ¥â¬Â§Ã§ÂºÅ Ã¥ÂÅ¡375*500Ã¥Â·Å Ã¥ÂÂ³Ã¯ÅÂ
#Ã¥ÂÂºÃŠÂÂ¬Ã€ÅŸÂÃ€ÅÂÃ¥ÂÂÃ¥Â·Â®ÃšÂ¶ÂÃšÂ¿Â100Ã£ÂÂÃ¯ÅÂÃ¥ÂÅ¡Ã€Â¹ÂÃ¥ÂÂÃ§ÂÂÃšÂ®Â­Ã§Â»ÂÃ€ÅŸÂ­Ã¯ÅÂÃ§Â¬Â¬Ã€ÅŸÂÃŠÂ­Â¥Ã¥Â°Â±ÃŠÂÂ¯Ã¥Â°ÂÃšÂ¿ÂÃ€ÂºÂÃ¥ÂÅžÃ§ÂÂÃ©ÂÅresizeÃ¥ÂÂ°300*300ÃŠÂÂÃŠÂÂ¯500*500Ã¯ÅÂÃŠÂÂÃŠÂÂÃ¥ÂÂÃ¥Â§ÂÃ¥ÂÅžÃ§ÂÂÃ€ÅŸÂÃšÂÅÃ§Å Â»ÃšÂ¿ÂÃ€ÅŸÂªÃŠÂ ÂÃ¥ÂÂÃšÂ¿ÂÃšÂ¿ÂÃ£ÂÂ
def resizeAllTheImages():
  path = os.path.join(destVOCImagePath + "/" + "JPEGImages")
  images = os.listdir(path)
  for aFile in images:
    img=Image.open(os.path.join(path,aFile))
    out = img.resize((img.size[0]/10,img.size[1]/10))
    out.save(os.path.join(path,aFile))
  print "resizeAllTheImages is done"

def resizeAllTheImagesMark():
  path = os.path.join(destVOCImagePath + "/" + "JPEGImagesMark")
  images = os.listdir(path)
  for aFile in images:
    img=Image.open(os.path.join(path,aFile))
    out = img.resize((img.size[0]/10,img.size[1]/10))
    out.save(os.path.join(path,aFile))

  print "resizeAllTheImagesMark is done"




if __name__ == '__main__':
  generateVOCDir()
  generateVOCJPEGImages()
  resizeAllTheImages()
  resizeAllTheImagesMark()
  os.system('cp ' + imgDir + "fromsrc2desImagess00012.map " + imgDir + "fromsrc2desImagess00012.map.backup")

