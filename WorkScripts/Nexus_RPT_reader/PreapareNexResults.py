import datetime
import pandas as pd
import os.path



def ReadFileForField(fileIn):
    # Cumulative Production Oil MSTB
    # Cumulative Production Gas MMSCF
    # Cumulative Production Water MSTB
    # Cumulative Injection Gas MMSCF
    # Cumulative Injection Water MSTB
    # Production Rate Oil STB/D
    # Production Rate Gas MSCF/D
    # Production Rate Water STB/D
    # Injection Rate Gas MSCF/D
    # Injection Rate Water STB/D
    # Gaslift Rate - MSCF/D
    # Cumulative Gaslift - MMSCF
    # Gas Oil Ratio MSCF/STB
    # Water Oil Ratio STB/STB
    # Water Cut - STB/STB
    # Recovery OOIP - %
    # Ave.Wt. Pressure Tot-PV PSIA
    # Ave.Wt. Pressure HCPV+ PSIA
    # CPU TIME - Seconds;Elapsed TIME - Seconds

    curDate = datetime.datetime.now()
    rowIndx = 0

    #with open(fileIn, "r") as fl:

    pd1=pd.read_csv(fileIn,";")



    f = open('text.txt', 'w')

    f.write("{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15};{16};{17}\n".format("Num", "Date", "Group",
         "FOPT", "FGPT", "FWPT", "FGIT", "FWIT", "FOPR", "FGPR", "FWPR", "FGIR", "FWIR", "GASLIFTRATE",
         "GASLIFTTOT", "FWCT", "Pressure_Tot-PV", "Pressure_HCPV"))

    pd1["Cumulative Production Oil MSTB"] *= 1000
    pd1["Cumulative Production Gas MMSCF"] *= 1000
    pd1["Cumulative Production Water MSTB"] *= 1000
    pd1["Cumulative Injection Gas MMSCF"] *= 1000
    pd1["Cumulative Injection Water MSTB"] *= 1000
    pd1["Production Rate Oil STB/D"] *= 1
    pd1["Production Rate Gas MSCF/D"] *= 1
    pd1["Production Rate Water STB/D"] *= 1
    pd1["Injection Rate Gas MSCF/D"] *= 1
    pd1["Injection Rate Water STB/D"] *= 1
    pd1["Gaslift Rate - MSCF/D"] *= 1
    pd1["Cumulative Gaslift - MMSCF"] *= 1
    pd1["Water Cut - STB/STB"] *= 1
    pd1["Ave.Wt. Pressure Tot-PV PSIA"] *= 1
    pd1["Ave.Wt. Pressure HCPV+ PSIA"] *= 1

    for e1 in pd1["Date"]:
        e2 = ConvertDate(e1)

        #print(e1 + "  " + e2)

        if e2 != curDate:
            #if(e2.day == 1):
                #print(str(rowIndx) + "  " + str(e2.__format__("%d.%m.%Y")) + "  " + str(pd1.at[rowIndx, "Cumulative Production Oil MSTB"]))
                f.write("{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15};{16};{17}\n".format(rowIndx, e2.__format__("%d.%m.%Y"), "Field",
                                             pd1.at[rowIndx, "Cumulative Production Oil MSTB"],
                                             pd1.at[rowIndx, "Cumulative Production Gas MMSCF"],
                                             pd1.at[rowIndx, "Cumulative Production Water MSTB"],
                                             pd1.at[rowIndx, "Cumulative Injection Gas MMSCF"],
                                             pd1.at[rowIndx, "Cumulative Injection Water MSTB"],
                                             pd1.at[rowIndx, "Production Rate Oil STB/D"],
                                             pd1.at[rowIndx, "Production Rate Gas MSCF/D"],
                                             pd1.at[rowIndx, "Production Rate Water STB/D"],
                                             pd1.at[rowIndx, "Injection Rate Gas MSCF/D"],
                                             pd1.at[rowIndx, "Injection Rate Water STB/D"],
                                             pd1.at[rowIndx, "Gaslift Rate - MSCF/D"],
                                             pd1.at[rowIndx, "Cumulative Gaslift - MMSCF"],
                                             pd1.at[rowIndx, "Water Cut - STB/STB"],
                                             pd1.at[rowIndx, "Ave.Wt. Pressure Tot-PV PSIA"],
                                             pd1.at[rowIndx, "Ave.Wt. Pressure HCPV+ PSIA"]))

        curDate = e2
        rowIndx += 1

    f.close()

    print("Done.")


def ReadFileForWells(fileIn, fileOut):
    # COP    # CGP    # CWP    # CGI    # CWI
    # QOP    # QGP    # QWP    # QGI    # QWI
    # BHP    # WPH    # WKH    # WPAV   # THP
    # COWP   # QOWP   # GOR    # WCUT   # WOR
    # QGLG   # CGLG   # DRDN   # DRMX   # CROP
    # CRGP   # CRWP   # CROI   # CRGI   # CRWI
    # ROP    # RGP    # RWP    # ROI    # RGI    # RWI
    # ONTM   # ALQ    # API    # QCDP   # CCDP   # YCDP
    # ACTV   # STAT   # SAL
    # Q1P    # Q1I    # C1P    # C1I    # X1P    # Y1P
    # Q2P    # Q2I    # C2P    # C2I    # X2P    # Y2P
    # Q3P    # Q3I    # C3P    # C3I    # X3P    # Y3P
    # Q4P    # Q4I    # C4P    # C4I    # X4P    # Y4P
    # Q5P    # Q5I    # C5P    # C5I    # X5P    # Y5P
    # Q6P    # Q6I    # C6P    # C6I    # X6P    # Y6P
    # Q7P    # Q7I    # C7P    # C7I    # X7P    # Y7P
    # Q8P    # Q8I    # C8P    # C8I    # X8P    # Y8P

    colNum = 0
    colDelta=93

    if os.path.exists(fileOut):
        os.remove(fileOut)

    pd1=pd.read_csv(fileIn,"\t")
    pd1=pd1.drop(columns=["TIME"])
#
    # pd2 = pd1.iloc[:, 0:94]
    # well = pd2.iat[0, 2]
    # pd2.insert(0, "Well", well)
    # pd2=pd2.loc[1:]
#
    # pd3=pd1.iloc[:,94:187]
    # well = pd3.iat[0, 2]
    # pd3.insert(0, "Well", well)
    # pd3 = pd3.loc[1:]
    # pd3.insert(1, "YEARS", pd1["YEARS"])

    for i1 in range(0,137):
        c1 = i1*colDelta+1
        c2 = c1 + colDelta

        pd3 = pd1.iloc[:, c1:c2]
        well = pd3.iat[0, 2]
        pd3.insert(0, "Well", well)
        pd3 = pd3.loc[1:]

        pd3.insert(1, "YEARS", pd1["YEARS"])
        if i1 != 0:
            #pd3.insert(1, "YEARS", pd1["YEARS"])
            pd3.to_csv(fileOut, mode='a', header=False)
        else:
            pd3.to_csv(fileOut, mode='a')

        print("Write well: " + well)

    #print(pd3.head())
        #print(str(c1) + "  " + str(c2))
    #print(str(pd3.count) + "  " + str(pd3.columns))

    print("Done.")


def ConvertDate(date):
    res=datetime.datetime.now()

#Tue Jan 01 00:00:00 GST 1991
    date = date.replace("Jan", "01")
    date = date.replace("Feb", "02")
    date = date.replace("Mar", "03")
    date = date.replace("Apr", "04")
    date = date.replace("May", "05")
    date = date.replace("Jun", "06")
    date = date.replace("Jul", "07")
    date = date.replace("Aug", "08")
    date = date.replace("Sep", "09")
    date = date.replace("Oct", "10")
    date = date.replace("Nov", "11")
    date = date.replace("Dec", "12")

    date = date.replace(" 00:00:00 GST", "")
    date = date[4:]

    str1=datetime.datetime.strptime(str(date), '%m %d %Y')

    res = str1

    return res












def main():
    fileIn = "Book3.csv"
    ReadFileForField(fileIn)

    #fileIn = "Wells_Nexus.txt"
    #fileOut = "Wells.txt"
    #ReadFileForWells(fileIn, fileOut)


if __name__ == '__main__':
    main()
    pass