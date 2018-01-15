import os
from PIL import Image

path = "/root/work/img/correctIg/forTest"
des = "/root/work/img/testImages/"

def resizeAllTheImages():
  images = os.listdir(path)
  for aFile in images:
    img=Image.open(os.path.join(path,aFile))
    out = img.resize((img.size[0]/5,img.size[1]/5))
    out.save(os.path.join(des,aFile))
  print "resizeAllTheImages is done"
  


resizeAllTheImages()
