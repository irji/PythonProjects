import os

def main():

    #baseDir="D:\TestExport\Base\\"

    str1="D:\TestExport\Base\E\EDU7@FORTS\\"
    str11="D:\TestExport\Base\EDU7@FORTS.txt"

    str2="D:\TestExport\Base\E\EUU7@FORTS\\"
    str21="D:\TestExport\Base\EUU7@FORTS.txt"

    str3="D:\TestExport\Base\S\SIU7@FORTS\\"
    str31="D:\TestExport\Base\SIU7@FORTS.txt"

    ProcceingFiles(str1, str11)

    ProcceingFiles(str2, str21)

    ProcceingFiles(str3, str31)

#f

def ProcceingFiles(dirs, result):
    #dirs = "D:\Programs\S\SIU7@FORTS\\"
    files = os.listdir(dirs)

    #resFile=open("D:\Programs\S\\result.txt", 'w')
    resFile = open(result, 'w')

    resFile.write("Date,Time,BestAsk,BestBid\n")

    for fldr in files:

        if fldr != "quotesCsvDates.txt":

            print(fldr)

            with open(dirs + fldr + "\\quotes.csv") as f:
                buyStr=""
                curStr=""

                lines = f.read().splitlines()

                for ln in lines:
                    s = ln.split(';')
                    date=fldr[8:10] + "." + fldr[5:7] + "." + fldr[:4] #разбираем строчку с датой на нормальную дату
                    hours=int(s[0][:2])+3

                    if hours > 9:
                        time=str(hours) + ":" + s[0][2:4] + ":" + s[0][4:6] #+ "." + s[0][6:] #собираем строчку с текущим временем
                        #resFile.write(date + ";" + s[0] + ";" + s[1] + ";" + s[2] + ";" + s[4] + ";" + time +"\n")
                        #resFile.write(date + ";" + time + ";" + s[2] + ";" + s[4] + "\n")

                        if s[4] == "Buy":
                            buyStr=s[2]
                        else:
                            if time not in curStr:  #s.find("is") == -1:
                                resFile.write(date + "," + time + "," + buyStr + "," + s[2] + "\n")
                                curStr=date + "," + time + "," + buyStr + "," + s[2] + "\n"

    resFile.close()

    print("Done!")


if __name__ == '__main__':
    main()
    pass