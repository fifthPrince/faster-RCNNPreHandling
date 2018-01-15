import os

s0009_valFile = open('../img/VOC2012/ImageSets/Main/s0009_val.txt','r')
srcFilePath = '/home/hone/miniconda2/lib/python2.7/site-packages/tensorflow/models/research/eguanwu_tielu2/img/VOC2012/JPEGImages/'
desFilePath = '/home/hone/miniconda2/lib/python2.7/site-packages/tensorflow/models/research/eguanwu_tielu2/img/testImages/'
allValFiles = []

for line in s0009_valFile.readlines():
  (fileName,yesorno) = line.split(" ")
  allValFiles.append(fileName.strip())


for image in allValFiles:
  os.system('cp ' + srcFilePath + image + '.jpg ' + desFilePath)
