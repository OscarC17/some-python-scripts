from os import listdir, chdir, rename
from os.path import isfile, join
from time import sleep

mypath = input("directory: ")
name = input("name: ")

chdir(mypath)
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(onlyfiles)
for x in range(0, len(onlyfiles)):
    if("png" in onlyfiles[x]):
        rename(onlyfiles[x], name + "_" + str(x) + ".png")
    elif("jpg" in onlyfiles[x]):
        rename(onlyfiles[x], name + "_" + str(x) + ".jpg")
    
sleep(2)