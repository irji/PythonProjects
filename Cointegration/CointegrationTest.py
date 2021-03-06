import statsmodels.tsa.stattools as ts
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import johansen as jo


def main():
 Coint1()

def Coint1():
 # #print('Hi!')
 #
 x1 = np.random.normal(0, 1, 250) #[1, 2, 3, 4, 5]
 x2 = np.random.normal(0, 1, 250) # [2, 4, 1, 5, 6]
 coin_result = ts.coint(x1, x2)
 print(coin_result)
 #
 #data1 = web.DataReader('FB', data_source='yahoo',start='4/4/2015', end='4/4/2016')
 #data2 = web.DataReader('AAPL', data_source='yahoo',start='4/4/2015', end='4/4/2016')
 #data1['key']=data1.index
 ##['key']=data2.index
 #
 #result = pd.merge(data1, data2, on='key')
 #
 #x1=result['Close_x']
 #y1=result['Close_y']
 #coin_result = ts.coint(x1, y1)
 # from statsmodels.tsa.stattools import coint
 # import pandas as pd
 # import pandas_datareader.data as web
 # import datetime as dt
 #
 # start = dt.datetime(2018, 1,1)
 # end = dt.datetime.today()
 #
 # intquery1 = web.DataReader(['HEI.DU','HEI.BE'], 'yahoo', start, end) ##<<<<<put start to finish date.
 # int1 = intquery1['Adj Close']
 #
 # print('############THIS cointegration on prices#####################')
 # score, pvalue, _ = coint(int1['HEI.DU'], int1['HEI.BE'])
 # print ('this is the coint score =',score,'\nthis is the pvalue =', pvalue,
 #        '\nthis is the 1% 5% & 10% = ',_)
 #
 #
 # df_normalize = (int1[:] / int1[:].shift(1) - 1).fillna(0)
 #
 # print('############THIS cointegration on Daily percetage move#####################')
 # score, pvalue, _ = coint(df_normalize['HEI.DU'], df_normalize['HEI.BE'])
 # print ('this is the coint score =',score,'\nthis is the pvalue =', pvalue,
 #        '\nthis is the 1% 5% & 10% = ',_)

def Coint2():
    x1 = np.random.normal(0, 1, 250)  # [1, 2, 3, 4, 5]
    x2 = np.random.normal(0, 1, 250)  # [2, 4, 1, 5, 6]
    coin_result = jo(x1, model=2, significance_level=0)

    eigenvectors, r = jo.johansen()

    print("r values are: {}".format(r))

    vec = eigenvectors[:, 0]
    vec_min = np.min(np.abs(vec))
    vec = vec / vec_min

    print("The first cointegrating relation: {}".format(vec))

    print(coin_result)


if __name__ == '__main__':
    main()
    pass