# -*- coding: UTF-8 -*-

import os

if(os.path.exists("glass.txt")): 
    os.remove("glass.txt")
    print("glass.txt已存在，所以删除")

if(os.path.exists("noGlass.txt")): 
    os.remove("noGlass.txt")
    print("noGlass.txt已存在，所以删除")

f = open("D:/CelebA/Anno/list_attr_celeba.txt")
newTxt = "glass.txt"
newf = open(newTxt, "a+")
newNoTxt = "noGlass.txt"
newNof = open(newNoTxt, "a+")

line = f.readline() 
line = f.readline() 
line = f.readline() 

glassCnt = 0
NoGlassCnt = 0

while line:
    array = line.split()
    #print(array[0])
    if (".jpg" in array[0] == False):
        print("no .jpg") 
        continue
    if (array[16] == "-1"): 
        new_context = array[0] + '\n'
        NoGlassCnt = NoGlassCnt + 1
        newNof.write(new_context)
    else: 
        new_context = array[0] + '\n'
        glassCnt = glassCnt + 1
        newf.write(new_context)
    line = f.readline()

print ("There are %d lines in %s" %(glassCnt, newTxt)) 
print ("There are %d lines in %s" %(NoGlassCnt, newNoTxt)) 

f.close()
newf.close()
newNof.close()