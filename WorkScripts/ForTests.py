import os
import numpy as np

dx = 42
dy = 74
dz = 150

# x1 = np.array(466200 * [0])
# x2 = np.zeros(466200)

x1 = np.array(dy * [np.zeros(dx)])
x3 = np.array(dz * [x1])

# x1 = np.array( [42 * [0], 74 * [0]])
inFile = "D:/Work/Models/Designer/Rus/Siec/Astoh/01_Astokh/Appendixes/Appendix2_Static_input/02_Export_from_MoReS/ECL.NNC"

with open(inFile) as fl:
    lines = fl.read().splitlines()

    for ln in lines:
        if ln.lstrip().find("NNC") == -1:
            coord = ln.lstrip().split()
            if len(coord) > 0:
                if coord[0].isdigit() == True:
                    #print("Cell {} {} {}".format(coord[0], coord[1], coord[2]))
                    #index = int(coord[0]) * int(coord[1]) * int(coord[2])
                    c1 = int(coord[0]) - 1
                    c2 = int(coord[1]) - 1
                    c3 = int(coord[2]) - 1

                    c4 = int(coord[3]) - 1
                    c5 = int(coord[4]) - 1
                    c6 = int(coord[5]) - 1

                    x3[c3][c2][c1] = 1
                    x3[c6][c5][c4] = 1

                    #index = int(coord[3]) * int(coord[4]) * int(coord[5])
                    #x3[index] = 1
#          print("Cell {} {} {}".format(coord[0], coord[1], coord[2]))

#x3 = x3.reshape(150,dx*dy)
x3 = x3.ravel()
np.savetxt("Prop1.txt", (x3), newline="\n", header="Prop1", footer="/")

# print(x3)
