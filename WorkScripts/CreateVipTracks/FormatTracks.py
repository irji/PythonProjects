import datetime
import pandas as pd
import os.path

def ConvertTrack(fileIn, fileOut):
    colNum = 0
    colDelta=93

    if os.path.exists(fileOut):
        os.remove(fileOut)

    resFile = open(fileOut, 'w')

    with open(fileIn) as f:
        ar2 = {}  # создаем пустой словарь
        wname = "-1"
        lines = f.read().splitlines()[1:]

        for ln in lines:
            s = ln.replace("\t", " ").split(' ', -1)

            if wname != str(s[0]):
                wname = str(s[0])
                resFile.write(";\nWELLTRACK " + wname + "\n" + s[1] + " " + s[2] + " " + s[3] + " " + s[4] + " " + "\n")
                #print(wname)
            else:
                resFile.write(s[1] + " " + s[2] + " " + s[3] + " " + s[4] + " " + "\n")

    print("Done.")


def main():
    # fileIn = "Dev_Profiles_COND_Model.txt"
    # fileOut = "Dev_Profiles_COND_Model_converted.txt"

    fileIn = "North_OBS_Well_Profiles.txt"
    fileOut = "North_OBS_Well_Profiles_converted.txt"

    ConvertTrack(fileIn, fileOut)


if __name__ == '__main__':
    main()
    pass