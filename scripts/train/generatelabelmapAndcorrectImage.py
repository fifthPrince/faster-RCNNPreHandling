import os
import generateVOCConfigFile
#fid = open('img/objnamemapping.log','r')

workpath = os.getenv("WORKPATH")

imgDir = workpath + '/img/'
outputfid = open('../img/tielu_label_map.pbtxt','w')

def generateLabelMap():
  imageDesFile = open(imgDir + "imageDescriptor","r")
  obj2filemapDic={}
  for line in imageDesFile.readlines():    
    (rPath,oldFileName,newFileName,oldObjName,newObjectName,location) = line.split(":")    
    if obj2filemapDic.has_key(generateVOCConfigFile.faultyName):
      obj2filemapDic[generateVOCConfigFile.faultyName].append(newFileName[:-4])
    else:
      obj2filemapDic[generateVOCConfigFile.faultyName]=[newFileName[:-4]]
  print obj2filemapDic

  

  correctImageDesFile = open("/root/work/img/correctIg/correctImageDescriptor","r")
  for line in correctImageDesFile:
    print line
    (fileName,objName,location,width,height) = line.split(":")
    loc = location.strip()[1:-1]
    locList = loc.split(",")
    x0 = locList[0].strip()
    y0 = locList[1].strip()
    x1 = locList[2].strip()
    y1 = locList[3].strip()
    if obj2filemapDic.has_key(generateVOCConfigFile.correctName):
      obj2filemapDic[generateVOCConfigFile.correctName].append(newFileName[:-4])
    else:
      obj2filemapDic[generateVOCConfigFile.correctName]=[newFileName[:-4]]
  correctImageDesFile.close()

  i = 1
  for key,values in obj2filemapDic.items():
    
    itemstring = 'item {\n  \
  id: ' + str(i) + ' \n   \
  name: \'' + key + '\' \n \
}'   
    outputfid.write(itemstring + '\n')
    i += 1


  outputfid.close()



if __name__ == '__main__':
  generateLabelMap()
