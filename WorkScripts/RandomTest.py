import numpy.random as np
import numpy as np1
import os

# for i in range(0, 10000000001):

num=10000000

with open("Log.txt", "w") as fl:
    fl.write("PORO\n")

res = np1.ndarray.tolist(np.uniform(0.1, 0.3, num))

for i in range(0,num):
    s = str(format(res[i], ".3f")) # + " " + str(res[i + 1]) + " " + str(res[i+2]) + " " + str(res[i+3])

#    if i+4<num:
#        i=i+4

    with open("Log.txt", "a") as fl:
        fl.write(s + "\n")
