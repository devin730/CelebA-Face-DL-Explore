import os
import shutil

nof = open("noGlass.txt")
hasf = open("glass.txt")

noLine = nof.readline() 
hasLine = hasf.readline() 

dir = ".\Img\img_align_celeba\img_align_celeba"
list = os.listdir(dir)
print(len(list))
hasGo = True
noGo = True

Cnt_get_hasGlass_image = 0
Cnt_get_noGlass_image = 0

for i in range(0, len(list)):
    imgName = os.path.basename(list[i])
    if (os.path.splitext(imgName)[1] != ".jpg"): continue

    noArray = noLine.split()
    if (len(noArray) < 1): noGo = False
    hasArray = hasLine.split()
    if (len(hasArray) < 1): hasGo = False

    while(int(os.path.splitext(imgName)[0]) > int(os.path.splitext(noLine)[0]) and noGo ):
        noLine = nof.readline()
        noArray = noLine.split()

    while(int(os.path.splitext(imgName)[0]) > int(os.path.splitext(hasLine)[0]) and hasGo ):
        hasLine = hasf.readline()
        hasArray = hasLine.split()

    print(imgName,noLine,hasLine)

    if (noGo and (imgName == noArray[0])):
        oldname= dir + "/" + imgName
        newname="./noGlass/"+imgName
        shutil.move(oldname, newname)
        Cnt_get_noGlass_image = Cnt_get_noGlass_image + 1
        noLine = nof.readline()
    elif (hasGo and (imgName == hasArray[0])):
        oldname= dir + "/" + imgName
        newname="./hasGlass/"+imgName
        shutil.move(oldname, newname)
        Cnt_get_hasGlass_image = Cnt_get_hasGlass_image + 1
        hasLine = hasf.readline()
    

print("处理了没有戴眼镜的照片 %d 张" %Cnt_get_noGlass_image)
print("处理了戴眼镜的照片 %d 张" %Cnt_get_hasGlass_image)

nof.close()
hasf.close()