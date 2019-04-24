import pandas as pd

def GetKeywordLines(fileIn, keywordOpen, linecount):
    count = 0
    res = ""
    date1 = "01.01.1960"

    lines = open(fileIn, "r").readlines()
    maxLine = len(lines)

    for indx, line in enumerate(lines):
        ln = line.strip().split()

        if len(ln) > 0:
            if ln[0] == "DATE":
                date1 = ln[1] + "." + ln[2] + "." + ln[3]

            #if (keywordOpen + " ") in line.strip():
            if line.find(keywordOpen) == 0:
                count += 1
                if indx + linecount <= maxLine:
                    keywordArray = []

                    for i in range(0, linecount+1):
                        ar1 = lines[indx + i].replace(keywordOpen, "").strip().replace("  ", " ", 1000).replace("\t", " ", 1000).split()
                        if i > 0:
                            if keywordOpen == "WLIMIT" or keywordOpen == "GLIMIT":
                                x1=["0"]
                                ar1 = x1 + ar1
                        keywordArray.append(ar1)

                    res = res + "\n" + create_keyword_table(date1, keywordArray, keywordOpen)

    if count > 0:
        _resFile = open(keywordOpen + ".txt", 'w')
        _resFile.write(res)
        _resFile.close()


    # with open(fileIn, "r") as fl:
    #     for line in fl:
    #
    #         ln = line.strip().split()
    #
    #         if len(ln) > 0:
    #             #if ln[0].isalpha():
    #                 if ln[0] == "DATE":
    #                     date1 = ln[1] + "." + ln[2] + "." + ln[3]
    #
    #                 if keywordOpen in line:
    #                     flag = True
    #                     count += 1
    #                     print(date1 + "  " + line, end='')
    #                 else:
    #                     if flag == True:
    #                         print(date1 + "  " + line, end='')
    #                         flag = False
    #         #else:
    #         #    flag = False

    print("Done. Num of " + keywordOpen + " keywords: " + str(count))



def create_keyword_table(date, keywordArray, keyword):
    res = ""
    phase = ""
    cond = ""

    condDic = {
        'STD': 'STD',
        'RES': 'RES',
        'FSTD': 'FSTD',
        'FRES': 'FRES',
    }

    if keyword == "YINJ":
        pd1 = pd.DataFrame(keywordArray[0])
        pd1.insert(0, "date", date)

        for indx, comp in enumerate(keywordArray[1]):
            pd1["comp" + str(indx)] = comp
    else:
        if keyword == "PROD" or keyword == "INJ" or keyword == "ECOLIM" or keyword == "WLIMIT" or keyword == "GLIMIT":
            phase = keywordArray[0][0]

            if keywordArray[0][1] in condDic:
                cond = keywordArray[0][1]
            else:
                cond = ""

        pd1 = pd.DataFrame(keywordArray)
        pd1 = pd1.transpose()
        pd1.insert(0, "date", date)

        if keyword == "PROD" or keyword == "INJ" or keyword == "ECOLIM" or keyword == "WLIMIT" or keyword == "GLIMIT":
            pd1.insert(1, "type", keyword)
            pd1.insert(2, "phase", phase)
            pd1.insert(3, "cond", cond)

#            if keyword == "WLIMIT":
#                pd1[-1] = keywordArray[1][0]

            if keywordArray[0][1] in condDic:
                pd1 = pd1.drop(pd1.index[0:2])
            else:
                pd1 = pd1.drop(pd1.index[0:1])

#        if keyword == "ECOLIM" or keyword == "WLIMIT":
#            pd1.insert(1, "phase", keywordArray[0][0])

            ## Get names of indexes for which column Age has value 30
            #indexNames = dfObj[dfObj['Age'] == 30].index
            ## Delete these row indexes from dataFrame
            #dfObj.drop(indexNames, inplace=True)

            #indexNames = pd1[pd1[0] != phase].index

            #indexNames = pd1.index[pd1["0"] == phase].tolist()

            #pd1.drop(indexNames, inplace=True)
            #print()


    res = pd1.to_string(index=False, header=False)

    return res



def main():
    fileIn = "PWF19COr.dat"
    #fileIn = "BFN_existing_wells_constraints_COMP_V2.inc"

    keywords = [
        ("PROD", 0),
        ("INJ", 0),
        ("QMAX", 1),
        ("QMIN", 1),
        ("QMULT", 3),
        ("YINJ", 1),
        ("BHP", 1),
        ("THP", 1),
        ("ITUBE", 2),
        ("TUBE", 3),
        ("ECOLIM", 0),
        ("WLIMIT", 1),
        ("GLIMIT", 1),
        ("DIAM", 2),
        ("WKHMULT", 1)]

    for k in keywords:
        #print(k[0])

#входной файл, кл. слово, количество доп. строк для зачитывания
        #GetKeywordLines(fileIn, "PROD", 0)
        GetKeywordLines(fileIn, str(k[0]), int(k[1]))

    #GetKeywordLines(fileIn, "WLIMIT", 1)


if __name__ == '__main__':
    main()
    pass