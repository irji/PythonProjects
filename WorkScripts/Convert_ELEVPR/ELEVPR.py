import datetime
import os.path



def ConvertFile(fileIn):
    _lines = open(fileIn, "r").readlines()
    flag =False
    flName= ""

    for line in _lines:
        if line.find("ELEVPR") == 0:
            flag = True
            str1 = line.split()
            flName = str1[-1]

        if line.find("ENDELEVPR") == 0:
            flag = False

        if flag is True:
            #print(flName)
            str2 = line.split()
            if len(str2) >= 2:
                _resFile = open(flName + ".txt", 'a')
                _resFile.write(str2[1] + " " + str2[0] + "\n")
                _resFile.close()

    print("Done.")



def main():
    fileIn = "UL_wells_ELEVPR_UPD_2018.dat"
    ConvertFile(fileIn)


if __name__ == '__main__':
    main()
    pass