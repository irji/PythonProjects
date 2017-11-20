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
                ar2[s[2]+s[3]]=ln.replace(',1,',',').replace(',5,',',').replace(',15,',',').replace(',30,',',')
                #ar2[s[1] + s[2]] = ln.replace(',1,', ',').replace(',5,', ',').replace(',15,', ',').replace(',30,', ',')

                #s = ln.split(';')
                #ar2[s[0] + s[1]] = ln

            ar1.append(ar2)
    return ar1


def CutOffArrays(ar, i):
    res = set(ar[i].keys())

    for ar1 in ar:
        aaa = set(ar1.keys())
        res = res.intersection(aaa)

    f = open('text.txt', 'w')
    ssss = ""
    f.writelines('<TICKER>,<PER>,<DATE>,<TIME>,<CLOSE>\n')

    res = sorted(res)

    for arKeys in res:
        #for ar2 in ar:
        #    ssss = ssss + ar2[arKeys] + ","

        str1= (ar[0][arKeys]).split(',')
        str2=(ar[1][arKeys]).split(',')

        if '<TIME>' not in ar[0][arKeys]:
            #ssss='{0},{1},{2},{3}'.format('SPFB.SintED', str1[1], str1[2], str(round(float(str1[3])/float(str2[3]),4)))
            ssss = '{0},{1},{2},{3}   {4}'.format('SPFB.SintED', str1[1], str1[2], str(round(float(str1[3]) / float(str2[3]), 4)), str(ar[0][arKeys]) + str(ar[1][arKeys]))
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

    print("Done!")


if __name__ == '__main__':
    main()
    pass