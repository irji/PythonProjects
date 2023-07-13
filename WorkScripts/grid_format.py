import sys


def ProcessGrid(fileIn):
    result = ""

    shift_x = 0 #2519094.2511 # 2519094.251097
    shift_y = 0 # 8658083.81055 # 8658083.810547
    shift_z = 0

    coordX = []
    coordY = []
    coordZ = []

    flag = True
    top = True

    with open(fileIn, "r") as fl:
        for line in fl:
            if "C" not in line and "!" not in line:
                args = line.split()

                try:
                    if len(args) > 0:
                        if flag == True:
                            if top == True :
                                coordX.append(float(args[0]) + shift_x)
                                coordX.append(float(args[3]) + shift_x)

                                coordY.append(float(args[1]) + shift_y)
                                coordY.append(float(args[4]) + shift_y)

                                coordZ.append(float(args[2]) + shift_z)
                                coordZ.append(float(args[5]) + shift_z)

                                top = False
                            else:
                                coordX.append(float(args[3]) + shift_x)
                                coordX.append(float(args[0]) + shift_x)

                                coordY.append(float(args[4]) + shift_y)
                                coordY.append(float(args[1]) + shift_y)

                                coordZ.append(float(args[5]) + shift_z)
                                coordZ.append(float(args[2]) + shift_z)

                                top = True
                except:
                    print(line)
                    flag = False
                    #sys.exit()

    _resFile = open("D:/Models/Conversion/VIP_Model/2021.11.09 - VIP_model/HM/VIPGRIDDAT/Grid.txt", 'w')
    _resFile.write("CORNERS\n")

    for x1 in coordX:
        _resFile.write(str(x1) + "\n")
    for y1 in coordY:
        _resFile.write(str(y1) + "\n")
    for z1 in coordZ:
        _resFile.write(str(z1) + "\n")

    _resFile.write("/\n")
    _resFile.close()


def ProcessGrid2(fileIn):
    result = ""

    shift_x = 0 #2519094.2511 # 2519094.251097
    shift_y = 0 #8658083.81055 # 8658083.810547
    shift_z = 0

    mult = 1000

    flag = True

    _resFile = open("D:/Models/Conversion/VIP_Model/2021.11.09 - VIP_model/HM/VIPGRIDDAT/Grid.txt", 'w')
    _resFile.write("CORP\n")

    with open(fileIn, "r") as fl:
        for line in fl:
            if "C" not in line and "!" not in line:
                args = line.split()

                try:
                    if len(args) > 0:
                        if flag == True:
                            _resFile.write("{} {} {}   {} {} {}\n".format((float(args[0]) + shift_x)*mult,
                                           (float(args[1]) + shift_y)*mult, (float(args[2]) + shift_z),
                            (float(args[3]) + shift_x)*mult, (float(args[4]) + shift_y)*mult, (float(args[5]) + shift_z)))
                except:
                    print(line)
                    flag = False
                    #sys.exit()

    _resFile.write("/\n")
    _resFile.close()



def main():
    fileIn ="D:/Models/Conversion/VIP_Model/2021.11.09 - VIP_model/HM/VIPGRIDDAT/SECTOR_Model_CGC.corp"

    ProcessGrid2(fileIn)


if __name__ == '__main__':
    main()
    pass