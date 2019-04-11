import pandas


def main():
    _fileIn = "Krwoj1q_BFN.inc"
    _buffer = open(_fileIn).read()

    _resFile = open(_fileIn + "converted.inc", 'w')

    lines = open(_fileIn, "r").readlines()

    _dates = parce_to_dates(lines)

    _table = ""
    _perfData = ""

    for t1 in _dates:
        print(_date)

    _perfFile.write(_perfData)

    print("Done.")



def parce_to_dates(lines):
    _dates = []
    _substr = ""

    for ln in lines[:-1]: #бегаем до предпоследнего элемента
        if ln.__contains__("DATE"):
            _dates.append(_substr)
            _substr = ""
        _substr = _substr + ln
    else: #если последний
        _dates.append(_substr)

    return _dates



if __name__ == '__main__':
    main()
    pass