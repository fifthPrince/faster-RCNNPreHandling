from cv2 import imread 


imgDir = '/home/hone/miniconda2/lib/python2.7/site-packages/tensorflow/models/research/eguanwu_tielu4/img/'
originalImagePath = imgDir + 'originalimg/'
destVOCImagePath = imgDir + 'VOC2012'

imageDesFile = open(imgDir + "imageDescriptor","r")

for line in imageDesFile.readlines():    
    (rPath,oldFileName,newFileName,oldObjName,newObjectName,location) = line.split(":")    
    img = imread(imgDir + "VOC2012/JPEGImages/" + "00004.jpg")
    #print img.shape
    loc = location.strip()[1:-1]
    locList = loc.split(",")
    x0 = locList[0].strip()
    y0 = locList[1].strip()
    x1 = locList[2].strip()
    y1 = locList[3].strip()
    
    if(img.shape[1]<=int(x1) or img.shape[0]<=int(y1)):
      print "wrong " + rPath + ":" + oldFileName

print "done! everything is ok"
