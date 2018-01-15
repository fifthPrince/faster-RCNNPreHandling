import os
from PIL import Image

count = 0
file1 = open("correctImageDescriptor1","r")
file2 = open("correctImageDescriptor","w")

for line in file1.readlines():
    (fileName,objName,location,width,height)  = line.split(":")
    numwidth = int(width)
    numheight = int(height)
    loc = location.strip()[1:-1]
    locList = loc.split(",")
    x0 = locList[0].strip()
    y0 = locList[1].strip()
    x1 = locList[2].strip()
    y1 = locList[3].strip()
    x = int(x1)
    y = int(y1)
    if x>numwidth or y>numheight:
      print "file is bad", fileName
    
    if int(x0)>=20 and int(y0)>=20 and x < numwidth - 20 and y < numheight - 20:
      count += 1
      print line.strip()
      file2.write(line)
      img=Image.open(os.path.join('/root/work/img/correctIg/K605782_11/',fileName))
      out = img.resize((img.size[0]/5,img.size[1]/5))
      out.save(os.path.join('/root/work/img/VOC2012/JPEGImages/',fileName))
      
print count
print "dine"
