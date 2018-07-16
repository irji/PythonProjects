import os

dirs = "Jpeg/"
files = os.listdir(dirs)

#for fileName in os.listdir("."):
#    os.rename(fileName, fileName.replace("CHEESE_CHEESE_", "CHEESE_"))

i = 1

os.chdir(dirs)

for fl in files:
    os.rename(fl, str(i)+".jpg")
    i=i+1

print("Done!")
