'''
Created on May 30, 2015

@author: GKostin
'''
# if __name__ == '__main__':
#    pass
# print("Hello world");
# f = open('text.txt', 'r')

import os


def ReadAllFiles(files, dr):
    # lst={}  # create hash
    ar1 = []  # создаем пустой список

    for fl in files:

        print("Файл: " + fl)

        with open(dr + fl) as f:
            ar2 = {}  # создаем пустой словарь
            lines = f.read().splitlines()

            for ln in lines:
                #s = ln.split(',')
                #ar2[s[2]+s[3]]=ln.replace(',1,',',').replace(',5,',',').replace(',15,',',').replace(',30,',',')
                #ar2[s[1] + s[2]] = ln.replace(',1,', ',').replace(',5,', ',').replace(',15,', ',').replace(',30,', ',')

                s = ln.split(';')
                ar2[s[0] + s[1]] = ln

            ar1.append(ar2)
    return ar1


def CutOffArrays(ar, i):
    res = set(ar[i].keys())

    for ar1 in ar:
        aaa = set(ar1.keys())
        res = res.intersection(aaa)

    f = open('text.txt', 'w')
    ssss = ""

    for arKeys in res:
        for ar2 in ar:
            ssss = ssss + ar2[arKeys] + ","

        f.write(ssss + '\n')
        ssss = ""

    f.close()

    # return res


def main():
    dirs = "Data/"
    files = os.listdir(dirs)

    lst = ReadAllFiles(files, dirs)

    minValue = 1000000000000
    maxValue = 0
    indx = 0
    i = 0

    #     for ar in lst:
    #         if len(ar) < minValue:
    #             indx=lst.index(ar)
    #             minValue=len(ar)
    #
    #         if len(ar) > maxValue:
    #             #indx=lst.index(ar)
    #             maxValue=len(ar)

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

    # keyValue= lst.key()

    # print(str(minValue) + "  " + str(indx) + "  " + str(maxValue))

    print("Done!")


if __name__ == '__main__':
    main()
    pass



# file='Data\SPFB.GAZR(1).txt'
# with open(file) as f:
#        l = f.read().splitlines()
# for line in l:
#    print(line)

# print(ffff(10, 5))
