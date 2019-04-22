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
                        ar1 = lines[indx + i].replace(keywordOpen, "").strip().replace("  ", " ", 1000).split()
                        keywordArray.append(ar1)

                    res = res + "\n" + create_keyword_table(date1, keywordArray, keywordOpen)

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

    if keyword == "YINJ":
        pd1 = pd.DataFrame(keywordArray[0])
        pd1.insert(0, "date", date)

        for indx, comp in enumerate( keywordArray[1]):
            pd1["comp" + str(indx)] = comp
    else:
        if keyword == "PROD" or keyword == "INJ":
            #ln = str(keywordArray[0]).split()
            phase = keywordArray[0][0]
            cond = keywordArray[0][1]

        pd1 = pd.DataFrame(keywordArray)
        pd1 = pd1.transpose()
        pd1.insert(0, "date", date)

        if keyword == "PROD" or keyword == "INJ":
            pd1.insert(1, "type", keyword)
            pd1.insert(2, "phase", phase)
            pd1.insert(3, "cond", cond)
            pd1 = pd1.drop(pd1.index[0:2])

    res = pd1.to_string(index=False, header=False)

    return res



def main():
    fileIn = "NFN008IIr.dat"

#входной файл, кл. слово, количество доп. строк для зачитывания
    GetKeywordLines(fileIn, "DIAM", 2)


if __name__ == '__main__':
    main()
    pass