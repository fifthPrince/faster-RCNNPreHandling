

import re

#inputfile = open("/home/hone/work/ai/tieluProject/size25output1/valu_25size_1out_faster_nas.log")
inputfile = open("/home/hone/work/ai/tieluProject/classesImage/s0012_verify.log")
searchedStr = "\'detection_scores\': array(["
              
#searchedStr = "detection_scores"
allScores = []
for line in inputfile.readlines():
    index = line.find(searchedStr)
    print line
    if index != -1:        
        print line
        newline = line[index+len(searchedStr):-1]
        numIndex = newline.find(",")
        print newline[:numIndex]
        number = float(newline[:numIndex])
        allScores.append(number)
    else:
        continue
    
allScores.sort()
print allScores


if __name__ == '__main__':
    pass