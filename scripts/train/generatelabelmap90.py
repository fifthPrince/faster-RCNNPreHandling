

#fid = open('img/objnamemapping.log','r')
import os
workpath = os.getenv("WORKPATH")
imagepath = os.getenv("IMAGEPATH")
imgDir = workpath + "/" + imagepath + '/img/'
outputfid = open( imgDir + '/tielu_label_map.pbtxt','w')

def generateLabelMap():
  imageDesFile = open(imgDir + "imageDescriptor","r")
  obj2filemapDic={}
  for line in imageDesFile.readlines():    
    (rPath,oldFileName,newFileName,oldObjName,newObjectName,location) = line.split(":")    
    if obj2filemapDic.has_key(newObjectName):
      obj2filemapDic[newObjectName].append(newFileName[:-4])
    else:
      obj2filemapDic[newObjectName]=[newFileName[:-4]]
  print obj2filemapDic

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
