import pandas as pd
from csv import reader

def main():

    _files=['Krgo_2P_BFN.inc', 'Krwoj1q_BFN.inc', 'Krwoj2q_BFN.inc', 'Krwoj3qb_BFN.inc', 'Krwoj4q_BFN.inc', 'Krwoj5q_BFN.inc', 'Krwoj6qb_BFN_v2.inc']
    #_files = ['Krwoj1q_BFN.inc', 'Krwoj2q_BFN.inc', 'Krwoj3qb_BFN.inc', 'Krwoj4q_BFN.inc',
    #           'Krwoj5q_BFN.inc', 'Krwoj6qb_BFN_v2.inc']

    tbl = ""
    _resFile = open("converted.inc", 'w')

    for _fl in _files:
        #_fl = "Krwoj1q_BFN.inc"
        print("Конвертирую файл {}".format(_fl))
        tbl = tbl + read_rp_tables(_fl)

    _resFile.write(tbl)

    print("Done.")


def read_rp_tables(_fileIn):
    #_resFile = open(_fileIn + "_converted.inc", 'w')
    _lines = open(_fileIn, "r").readlines()

    _tables = parce_to_dates(_lines)

    print("Найдено {} таблиц".format(_tables.__len__()))

    _tb = "SWOF\n"

    for t1 in _tables:
        if len(t1) > 3:
            pd1 = pd.DataFrame(t1[1:], columns=['SW', 'KRW', 'KROW', 'PCWO'], dtype=float)
            _minVal = pd1['PCWO'].min()

            pd1['PCWO'] = pd1['PCWO'] - _minVal
            #pd1['TbEnd'] = '/'
            _tb = _tb + pd1.to_string(index=False, header=False) + "\n/\n"
            #print(pd1)
    #print(_tb)

    #_resFile.write(_tb)

    return _tb



def parce_to_dates(lines):
    _tables = []
    _substr = []

    for ln in lines:
        if ln.__contains__("SWT") or ln.__contains__("SGT"):
            if ln.startswith("!") == False:
                if len(_substr) > 0:
                    _tables.append(_substr)
                    _substr = []

        if ln.startswith("!") == False:
            if (ln.__contains__("SWT") == False) or (ln.__contains__("SGT") == False):
                ln = ln.strip().replace("\t", " ", 1000).replace("\n", "", 1000)
                ar1 = ln.split(" ")
                if len(ar1) > 3:
                    _substr.append(ar1)
    else:
        _tables.append(_substr)

    return _tables



if __name__ == '__main__':
    main()
    pass