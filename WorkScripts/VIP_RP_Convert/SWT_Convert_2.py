import pandas as pd
from csv import reader

def main():

    swt_file = "D:/test_gdwtable_hysteresis/nexus_data/VIPINCL/Krwoj1q.inc"
    sgt_file = "D:/test_gdwtable_hysteresis/nexus_data/VIPINCL/Krgo_2P.inc"

    read_rp_tables()

    #_resFile = open("converted.inc", 'w')

    print("Done.")


def read_rp_tables():
    swt_file = "D:/test_gdwtable_hysteresis/nexus_data/VIPINCL/Krwoj1q.inc"
    sgt_file = "D:/test_gdwtable_hysteresis/nexus_data/VIPINCL/Krgo_2P.inc"
    sgwt_file = "D:/test_gdwtable_hysteresis/nexus_data/VIPINCL/Krwgb.inc"

    swt_lines = open(swt_file, "r").readlines()
    sgt_lines = open(sgt_file, "r").readlines()
    sgwt_lines = open(sgwt_file, "r").readlines()

    swt_tables = parce_to_dates(swt_lines)
    sgt_tables = parce_to_dates(sgt_lines)
    sgwt_tables = parce_sgwt(sgwt_lines)


    #print("Найдено {} таблиц".format(swt_tables.__len__()))

    swt_tb = ""
    sgt_tb = ""
    sgwt_tb = ""

#    for t1 in swt_tables:
    for ind in range(len(swt_tables)):
        swt_tb = "WOTABLE\nSW KRW KROW PCWO\n"
        sgt_tb = "GOTABLE\nSG KRG KROG PCGO\n"
        sgwt_tb = "GDWTABLE\nSG KRWG\n"

        swt_pd1 = pd.DataFrame(swt_tables[ind], columns=['SW', 'KRW', 'KROW', 'PCWO'], dtype=float)
        swt_tb = swt_tb + swt_pd1.to_string(index=False, header=False) + "\n\n"

        sgt_pd1 = pd.DataFrame(sgt_tables[ind], columns=['SW', 'KRW', 'KROW', 'PCWO'], dtype=float)
        sgt_tb = sgt_tb + sgt_pd1.to_string(index=False, header=False) + "\n\n"

        sgwt_pd1 = pd.DataFrame(sgwt_tables[ind], columns=['SG', 'KRG'], dtype=float)
        sgwt_tb = sgwt_tb + sgwt_pd1.to_string(index=False, header=False) + "\n\n"

        #_tb = _tb + str(t1)

        _resFile = open("D:/test_gdwtable_hysteresis/nexus_data/VIPINCL/Tables/Table_" + str(ind + 1) + ".txt", 'w')
        _resFile.write(swt_tb + sgt_tb + sgwt_tb)
        _resFile.close()

        #print(swt_tb + sgt_tb + sgwt_tb)
        print("RELPM Method {} nexus_data/VIPINCL/Tables/Table_{}.txt".format(ind + 1, ind + 1))

    #_resFile.write(_tb)

    #return _tb


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

def parce_sgwt(lines):
    _tables = []
    _substr = []

    for ln in lines:
        if ln.__contains__("SGWT"):
            if ln.startswith("!") == False:
                if len(_substr) > 0:
                    _tables.append(_substr)
                    _substr = []

        if ln.startswith("!") == False:
            if (ln.__contains__("SGWT") == False):
                ln = ln.strip().replace("\t", " ", 1000).replace("\n", "", 1000)
                ar1 = ln.split(" ")
                #if len(ar1) > 3:
                _substr.append(ar1)
    else:
        _tables.append(_substr)

    return _tables


if __name__ == '__main__':
    main()
    pass