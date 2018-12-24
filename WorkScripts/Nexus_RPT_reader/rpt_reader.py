
def GetProdLimits(fileIn):
    count = 0
    newLine = ""
    flag = False
    date1 = ""

    with open(fileIn, "r") as fl:
        for line in fl:
            if "Maximum Surface Rate Constraints" in line:
                dt = line.split(" ")
                date1 = dt[-1].rstrip()

    #====================== разбор даты ===========================
#                dt2 = date1.split("/")
#                m1 = ""
#                d1 = ""
#
#                if int(float(dt2[1])) < 10:
#                    m1 = "0" + str(dt2[1]).replace("0","")
#                else:
#                    m1 = str(dt2[1])
#
#                if int(float(dt2[0])) < 10:
#                    d1 = "0" + str(dt2[0]).replace("0","")
#                else:
#                    d1 = str(dt2[0])
#
#                date1 = m1 + "." + d1 + "." + str(dt2[2])
    # =============================================================
                date1=ConvertDate(date1)

                count += 1

            if "CONNECTION       NUMBER      QOSMAX      QGSMAX      QWSMAX    QLIQSMAX    QMHCMAX     QALLRMAX" in line:
                flag = True

            if "==============" in line:
                flag = False

            if flag is True and len(line) > 1:
                newLine = ""

                for i in range(0, len(line), 12):
                    newLine = newLine + str(line[i:i + 12]).rstrip() + "|"

                print(date1 + "|" + newLine + '\n', end='')

    print("Done. Num of dates: " + str(count))

def GetPressLimits(fileIn):
    count = 0
    newLine = ""
    flag = False
    date1 = ""

    with open(fileIn, "r") as fl:
        for line in fl:
            if "Pressure Constraints at time" in line:
                dt = line.split(" ")
                date1 = dt[-1].rstrip()

    #====================== разбор даты ===========================
#                dt2 = date1.split("/")
#                m1 = ""
#                d1 = ""
#
#                if int(float(dt2[1])) < 10:
#                    m1 = "0" + str(dt2[1]).replace("0","")
#                else:
#                    m1 = str(dt2[1])
#
#                if int(float(dt2[0])) < 10:
#                    d1 = "0" + str(dt2[0]).replace("0","")
#                else:
#                    d1 = str(dt2[0])
#
#                date1 = m1 + "." + d1 + "." + str(dt2[2])
    # =============================================================
                date1 = ConvertDate(date1)

                count += 1

            if "NODE            NUMBER       PMIN      PMAX      PGMAX     PWMAX" in line:
                flag = True

            if "==============" in line:
                flag = False

            if flag is True and len(line) > 1:
                newLine = ""

                for i in range(0, len(line), 12):
                    newLine = newLine + str(line[i:i + 12]).rstrip() + "|"

                print(date1 + "|" + newLine + '\n', end='')

    print("Done. Num of dates: " + str(count))


def GetKeywordLines(fileIn, keywordOpen, keywordClose):
    count = 0
    newLine = ""
    flag = False
    date1 = ""

    with open(fileIn, "r") as fl:
        for line in fl:
            #if "TIME" in line:
            if line.find("TIME") == 0:
                dt = line.replace("\t", " ").split()#.split(" ")
                date1 = dt[1].rstrip()
                date1 = ConvertDate(date1)

# ищем кл. слово с учетом регистра
            if keywordOpen in line:
                flag = True
                #count += 1

            if keywordClose in line:
                flag = False
                count += 1

            if flag is True and len(line) > 1:
                #if "NAME" not in line and keywordOpen not in line:
                if keywordOpen not in line:
                    print(date1 + "  " + line, end='')

    print("Done. Num of keywords: " + str(count))



def GetElevationDH(fileIn):
    count = 0
    newLine = ""
    flag = False
    date1 = ""
    well_name = ""
    first_point1 = 0
    last_point1 = 0
    first_point2 = 0
    last_point2 = 0

    with open(fileIn, "r") as fl:
        for line in fl:

            if "ENDELEVPR" in line:
                flag = False

                #if well_name == "WHT4P-WHT6P":
                print(well_name + " TVD_start= " + str(first_point1) + " MD_start= " + str(first_point2) + " TVD_end= " + str(last_point1) + " MD_end= " + str(last_point2) +"\n", end='')

                first_point1 = 0
                last_point1 = 0
                first_point2 = 0
                last_point2 = 0

                #count += 1

            if flag is True and len(line) > 1 and "TVD" not in line:
                num1 = line.strip().replace("\t", " ").split()

                if int(float(num1[0])) >= 0 and first_point1 == 0 and first_point2 == 0:
                    #print(line)
                    #first_point = float(num1[1])
                    first_point1 = str(num1[0]).rstrip()
                    first_point2 = str(num1[1]).rstrip()

                if int(float(num1[0])) > 0:
                    last_point1 = str(num1[0]).rstrip()
                    last_point2 = str(num1[1]).rstrip()


                #if "NAME" not in line and keywordOpen not in line:
                #if keywordOpen not in line:
                #    print(date1 + "  " + line, end='')


            if "ELEVPR" in line and "ENDELEVPR" not in line:
                flag = True
                well_name = line.strip().replace("\t", " ").split()[-1]
                well_name = (well_name).rstrip()
                count += 1


    print("Done. Num of keywords: " + str(count))





def ConvertDate(strIn):

    strout=""

    dt2 = strIn.split("/")
    m1 = ""
    d1 = ""

    if int(float(dt2[1])) < 10:
        m1 = "0" + str(dt2[1]).replace("0", "")
    else:
        m1 = str(dt2[1])

    if int(float(dt2[0])) < 10:
        d1 = "0" + str(dt2[0]).replace("0", "")
    else:
        d1 = str(dt2[0])


    strout = m1 + "." + d1 + "." + str(dt2[2])

    return strout



def main():
    #fileIn = "UL_Nexus_model.rpt"
    fileIn = "UL_Surface_Nexus_Model.dat"
    #fileIn = "UL_wells_ELEVPR_UPD_2018.dat"

    #GetProdLimits(fileIn)

    #GetPressLimits(fileIn)

    #GetKeywordLines(fileIn, "TARGET", "ENDTARGET")
    GetKeywordLines(fileIn, "ACTIVATE", "ENDACTIVATE")

    #GetElevationDH(fileIn)


if __name__ == '__main__':
    main()
    pass