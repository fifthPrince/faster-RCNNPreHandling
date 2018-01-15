import os


file1 = open("/root/work/img/VOC2012/ImageSets/Main/faulty_val.txt","r")


for line in file1.readlines():
    (fileName,flag)  = line.split(":")
      if flag == '1':
        os.system("cp " + '/root/work/img/VOC2012/JPEGImages/' + fileName + ".jpg /root/work/img/testImages/" )


print "dine"
