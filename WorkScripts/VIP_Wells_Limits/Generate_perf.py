import pandas as pd
from datetime import datetime

def CreateCOMPDAT(fileIn):

    date = ""
    result = ""

    with open(fileIn, "r") as fl:
        for line in fl:
            if "--" not in line:
                args = line.split()

                if date != Convert_date(str(args[0])):
                    date = Convert_date(str(args[0]))
                    result = result + "DATES\n" + date + "  /\n/\n\n" + PerfData(args)
                    #result = result + "DATES\n" + date + "  /\n/\n\n" + Perf_LGR_Data(args)

                else:
                    result = result + PerfData(args)
                    #result = result + Perf_LGR_Data(args)

    _resFile = open("PERF3.txt", 'w')
    _resFile.write(result)
    _resFile.close()
    #print (result)

def Convert_date(dateIn):

    strout = datetime.strptime(dateIn, "%d.%m.%Y").date()
    strout2 = strout.strftime("%d %b %Y")

    return strout2

def PerfData(strIn):

    #ANGLA->AZM
    #ANGLV->INCL

    state = "OPEN"
    if str(strIn[5]) == "OFF" : state = "SHUT"

    ANGLV = "INCL"

    ANGLA = "AZM"


    #result = "COMPDAT\n" + "{} {} {} {} {} {} {}".format(str(strIn[1]), str(strIn[3]), str(strIn[4]), str(strIn[2]), str(strIn[2]), state, "2* 0.5 1* 0 /\n/\n\n")

    result = "COMPDAT\n" + "{} {} {} {} {} {} 2* {} 1* {} /\n/\n\n".format(str(strIn[1]), str(strIn[3]), str(strIn[4]), str(strIn[2]),
                                                         str(strIn[2]), state, 2*float(strIn[11]), str(strIn[12]))

    result = result + "COMPVAL\n" + "{} {} {} {} {} {} {} /\n".format(str(strIn[1]), str(strIn[3]), str(strIn[4]), str(strIn[2]), str(strIn[2]), ANGLV, str(strIn[9]))
    result = result + "{} {} {} {} {} {} {} /\n".format(str(strIn[1]), str(strIn[3]), str(strIn[4]),
                                                                           str(strIn[2]), str(strIn[2]), ANGLA,
                                                                           str(strIn[10]))

    result = result + "{} {} {} {} {} {} {} /\n/\n\n".format(str(strIn[1]), str(strIn[3]), str(strIn[4]),
                                                                           str(strIn[2]), str(strIn[2]), "LENGTH",
                                                                           str(strIn[7]))

    #result = result + "WPIMULT\n" + "{} {} {} {} {} /\n/\n\n".format(str(strIn[1]), str(strIn[3]), str(strIn[4]),
    #                                                                       str(strIn[2]), 2)

    return result

def Perf_LGR_Data(strIn):

    #ANGLA->AZM
    #ANGLV->INCL

    state = "OPEN"
    if str(strIn[10]) == "OFF" : state = "SHUT"

    ANGLV = "INCL"
    ANGLA = "AZM"

    #--Date WELL GRID IW JW L LENGTH PWDEP ANGLV ANGLA STAT SKIN RADW
    #result = "COMPDAT\n" + "{} {} {} {} {} {} {}".format(str(strIn[1]), str(strIn[3]), str(strIn[4]), str(strIn[2]), str(strIn[2]), state, "2* 0.5 1* 0 /\n/\n\n")

    result = "COMPDATL\n" + "{} {} {} {} {} {} {} 2* {} 1* {} /\n/\n\n".format(str(strIn[1]), str(strIn[2]), str(strIn[3]), str(strIn[4]),
                                                         str(strIn[5]), str(strIn[5]), state, 2*float(strIn[12]), str(strIn[11], ))

    result = result + "COMPVALL\n" + "{} {} {} {} {} {} {} {} /\n".format(str(strIn[1]), str(strIn[2]), str(strIn[3]), str(strIn[4]),
                                                                      str(strIn[5]), str(strIn[5]), ANGLV, str(strIn[8]))

    result = result + "{} {} {} {} {} {} {} {} /\n".format(str(strIn[1]), str(strIn[2]), str(strIn[3]), str(strIn[4]),
                                                                      str(strIn[5]), str(strIn[5]), ANGLA, str(strIn[9]))

    result = result + "{} {} {} {} {} {} {} {} /\n/\n\n".format(str(strIn[1]), str(strIn[2]), str(strIn[3]), str(strIn[4]),
                                                                      str(strIn[5]), str(strIn[5]), "LENGTH",
                                                                           str(strIn[6]))

    #result = result + "WPIMULT\n" + "{} {} {} {} {} /\n/\n\n".format(str(strIn[1]), str(strIn[3]), str(strIn[4]),
    #                                                                       str(strIn[2]), 2)

    return result

def main():
    fileIn ="Well_from_VIP_3.txt"

    CreateCOMPDAT(fileIn)


if __name__ == '__main__':
    main()
    pass