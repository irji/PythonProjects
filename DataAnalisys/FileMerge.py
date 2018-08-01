import os


def ReadAllFiles(files, dr):
    # lst={}  # create hash
    ar1 = []  # создаем пустой список
    names = ""

    for fl in files:

        print("Файл: " + fl)

        with open(dr + fl) as f:
            ar2 = {}  # создаем пустой словарь
            lines = f.read().splitlines()[1:]

            for ln in lines:
                s = ln.split(',')
                #ar2[s[2]+s[3]]=ln.replace(',1,',',').replace(',5,',',').replace(',15,',',').replace(',30,',',')
                ar2[s[2] + "," + s[3]] = s[4]

            ar1.append(ar2)
            names=names+","+str(s[0])

    tuple1=(names,ar1)

    #return ar1
    return tuple1


def CutOffArrays(ar, i):

    names=ar[0]
    dic1=ar[1]

    res = set(dic1[i].keys())

    for ar1 in dic1:
        aaa = set(ar1.keys())
        res = res.intersection(aaa)

    f = open('text.txt', 'w')
    ssss = ""

    f.write("Date,Time" + names + '\n')

    res = sorted(res)

    for arKeys in res:
        for ar2 in dic1:
            ssss = ssss + "," + ar2[arKeys]

        f.write(arKeys + ssss + '\n')
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
