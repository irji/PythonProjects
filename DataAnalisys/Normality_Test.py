import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

myFile = pd.read_csv('text.txt', sep=',')[13503:]

basis=(7*myFile['SPFB.GAZR']-1*myFile['SPFB.VTBR']).values
#basis=myFile['SPFB.LKOH']-4*myFile['SPFB.VTBR']+110000

print(basis)
#ccc=basis
#print(type(ccc[1]))

basis=sorted(basis)

ks_results = stats.kstest(basis, cdf='norm')
#dagostino_results = stats.normaltest(basis)


xxx=[]
yyy=[]
zzz=[]

#for x1 in range(1,11):
#    for y1 in range(1,11):

#        basis = x1 * myFile['SPFB.GAZR'] - y1 * myFile['SPFB.VTBR']

#        ks_results = stats.kstest(basis, cdf='norm')

#        xxx.append(x1)
#        yyy.append(y1)
#        zzz.append(dagostino_results[1])

#        if dagostino_results[1] > 0:
#            print(str(x1) + "," + str(y1))

#df=pd.DataFrame({'X1': xxx,'Y1': yyy, 'Normal': zzz})


#plt.plot(df['X1'])
#plt.plot(df['Y1'])
#plt.show()




print("KS: Test= " + str(ks_results[0]) + ", p-value= " + str(ks_results[1]))
#print("DP: Test= " + str(dagostino_results[0]) + ", p-value= " + str(dagostino_results[1]))

#np.random.seed(987654321)
#x=stats.t.rvs(100,size=100)
#print(stats.kstest(x,'norm'))

#plt.hist(basis,20)
#plt.show()

#print(x)