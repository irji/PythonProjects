import os

def ReadAllFiles(files, dr):
    ar1 = []  # создаем пустой список

    for fl in files:

        print("Файл: " + fl)

        with open(dr + fl) as f:
            ar2 = {}  # создаем пустой словарь
            lines = f.read().splitlines()

            for ln in lines:
                s = ln.split(',')
                #year=s[1][6:]
                #month=s[1][3:5]
                #day=s[1][0:2]

                key1=s[1][6:] + s[1][3:5] + s[1][0:2] + s[2].replace(':','')
                ar2[key1] = ln

            ar1.append(ar2)
    return ar1


def CutOffArrays(ar, i):
    res = set(ar[i].keys())

    for ar1 in ar:
        aaa = set(ar1.keys())
        res = res.intersection(aaa)

    f = open('text.txt', 'w')
    ssss = ""
    #f.writelines('<TICKER>,<PER>,<DATE>,<TIME>,<CLOSE>\n')

    res = sorted(res)

    for arKeys in res:
        #for ar2 in ar:
        #    ssss = ssss + ar2[arKeys] + ","

        str1= (ar[0][arKeys]).split(',')
        str2=(ar[1][arKeys]).split(',')

        if 'Time' not in ar[0][arKeys]:
            #ssss='{0},{1},{2},{3}'.format('SPFB.SintED', str1[1], str1[2], str(round(float(str1[3])/float(str2[3]),4)))
            ssss = '{0},{1},{2},{3},{4}'.format('SintED', str1[1], str1[2], str(round(float(str1[3]) / float(str2[3]), 4)), str(round(float(str1[4]) / float(str2[4]), 4)))
            f.write(ssss + '\n')
            ssss = ""

    f.close()

    # return res


def CutOffArrays2(ar, i):
    res = set(ar[i].keys())

    for ar1 in ar:
        aaa = set(ar1.keys())
        res = res.intersection(aaa)

    f = open('text2.txt', 'w')
    ssss = ""

    res = sorted(res)

    for arKeys in res:
        for ar2 in ar:
            ssss = ssss + ar2[arKeys] + ","

        f.write(ssss + '\n')
        ssss = ""

    f.close()


def main():
    #ED-9.17,14.07.2017,15:51:02,1.1544,1.1333

    files=['EU-9.17@FORTS.txt', 'SI-9.17@FORTS.txt']

    dirs = "D:/Source/Data/"
    #files = os.listdir(dirs)

    lst = ReadAllFiles(files, dirs)

    minValue = 1000000000000
    maxValue = 0
    indx = 0
    i = 0

    # calculating minimal length
    while i != len(lst):
        if len(lst[i]) < minValue:
            indx = i
            minValue = len(lst[i])

        if len(lst[i]) > maxValue:
            # indx=i
            maxValue = len(lst[i])

        i = i + 1

    # make all arrays of the same length
    CutOffArrays(lst, indx)

    files = ['ED-9.17@FORTS.txt', 'text.txt']

    dirs = "D:/Source/Data/D1/"
    # files = os.listdir(dirs)

    lst = ReadAllFiles(files, dirs)

    minValue = 1000000000000
    maxValue = 0
    indx = 0
    i = 0

    # calculating minimal length
    while i != len(lst):
        if len(lst[i]) < minValue:
            indx = i
            minValue = len(lst[i])

        if len(lst[i]) > maxValue:
            # indx=i
            maxValue = len(lst[i])

        i = i + 1

    # make all arrays of the same length
    CutOffArrays2(lst, indx)



    print("Done!")


if __name__ == '__main__':
    main()
    pass