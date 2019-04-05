# To get "WellDef" a regex "(WellDef.*(\n(.*|\n)*?}))" is used    DATE.*(\n(.*|\n)*?\s*(?=DATE))

import re

def main():
    #_fileIn = "RM2_HM_PVT_KV_27FEB_WELLS.ixf"
    _fileIn = "RM2_HM_PVT_KV_27FEB_WELL_CONNECTIONS.ixf"  # _perfFile
    _buffer = open(_fileIn).read()

    #_tableFile = open("PerfTable.txt", 'w')
    _perfFile = open("Perforation.txt", 'w')
    #_specFile = open("Specification.txt", 'w')

    #_wellPattern = re.compile('(WellDef.*{\\n(.*|\\n)*?})', re.MULTILINE) # возвращает tuple
    _wellPattern = re.compile('WellDef.*{(?:\\n(?:.*|\\n)*?})', re.MULTILINE) #в отличае от предыдущего возвращает строки

    #_datePattern = re.compile('DATE.*\\n(.*|\\n)*?.*(?=DATE)')
    _datePattern = re.compile('(\\b\\d{1,2}-+([A-Za-z]){3}-+\\d{1,4})|$')

    _wellNamePattern = re.compile('WellDef.*"(.*?)"', re.MULTILINE)
    _undefinedPattern = re.compile('Undefined="(.*?)"', re.MULTILINE)

    _wellToCellConnectionsPattern = re.compile('WellToCellConnections.*[[](\\n(.*|\\n)*?\\s*)[]]', re.MULTILINE)


    lines = open(_fileIn, "r").readlines()

    _dates = parce_to_dates(lines)

    _table = ""
    _perfData = ""

    for t1 in _dates:
        #_date = _datePattern.findall(t1)
        _dateSearch = re.search(_datePattern, t1)
        _date = _dateSearch.group()

        print(_date)

        if _date != "":
            _perfData = _perfData + "DATES\n" + _date.replace("-", " ") + "\n/\n\n"

        if len(_date) > 0:
            _well = _wellPattern.findall(t1)
            _perfData = _perfData + read_well_perf(_well, _undefinedPattern, _wellNamePattern, _wellToCellConnectionsPattern)
            #_table = _table + create_well_perf_table(_date, _well, _wellNamePattern, _wellToCellConnectionsPattern)


    #_tableFile.write(_table)
    _perfFile.write(_perfData)
    #_specFile.write(_perfData)




    #print(_dates)
#    print(_result.group(0))


    print("Done.")


def read_Well_Spec_Info(_wells, _date):

    line = ""

    _wellNamePattern = re.compile('WellDef.*"(.*?)"', re.MULTILINE)

    _headDensityCalculationPattern = re.compile('HeadDensityCalculation=([A-Za-z"]*)', re.MULTILINE)
    _allowCrossFlowPattern = re.compile('AllowCrossFlow="(.*?)"', re.MULTILINE)
    _pseudoPressureModelPattern = re.compile('PseudoPressureModel=([A-Za-z"]*)', re.MULTILINE)
    _frictionPattern = re.compile('Friction="(.*?)"', re.MULTILINE)
    _accelerationPattern = re.compile('Acceleration="(.*?)"', re.MULTILINE)

    _undefinedPattern = re.compile('Undefined="(.*?)"', re.MULTILINE)

    _wellToCellConnectionsPattern = re.compile('WellToCellConnections.*[[](\\n(.*|\\n)*?\\s*)[]]', re.MULTILINE)

    _constraintDevicePattern = re.compile('ConstraintDevice.*{(\\n(.*|\\n)*?\\s*)}', re.MULTILINE)
    _segmentNodesPattern = re.compile('SegmentNodes.*\[(\\n(.*|\\n)*?\\s*)\]', re.MULTILINE)
    _segmentPipesPattern = re.compile('SegmentPipes.*\[(\\n(.*|\\n)*?\\s*)\]', re.MULTILINE)

    _resVolConditionsPattern = re.compile('ResVolConditions.*{(\\n(.*|\\n)*?\\s*)}', re.MULTILINE)

    for _w in _wells:
        _wellName = _wellNamePattern.findall(_w)
        _headDensityCalculation= _headDensityCalculationPattern.findall(_w)
        _allowCrossFlow = _allowCrossFlowPattern.findall(_w)
        _pseudoPressureModel = _pseudoPressureModelPattern.findall(_w)
        _friction = _frictionPattern.findall(_w)
        _acceleration = _accelerationPattern.findall(_w)
        _undefined = _undefinedPattern.findall(_w)

        _wellToCellConnections = _wellToCellConnectionsPattern.findall(_w)

        _constraintDevice = str(_constraintDevicePattern.findall(_w)).replace("\\n","")
        _segmentNodes = _segmentNodesPattern.findall(_w)
        _segmentPipes = _segmentPipesPattern.findall(_w)

        _resVolConditions = _resVolConditionsPattern.findall(_w)

        line = line + '{} {} {} {} {} {} {} {} {} {} {} {} {}\n'.format(_date, _wellName, _headDensityCalculation, _allowCrossFlow, _pseudoPressureModel, _friction, _acceleration, _undefined, _wellToCellConnections,
                                                _constraintDevice, _segmentNodes, _segmentPipes, _resVolConditions)


    return line


def read_well_perf(_wells, _undefinedPattern, _wellNamePattern, _wellToCellConnectionsPattern):

    _perfData = ""

    for _w in _wells:
        _undefSearch = re.search(_undefinedPattern, _w)
        _undef = _undefSearch.group()

        _wellnameSearch = re.search(_wellNamePattern, _w)
        _wellname = _wellnameSearch.group()

        _wellToCellConnectionsSearch = re.search(_wellToCellConnectionsPattern, _w)
        _wellToCellConnections = _wellToCellConnectionsSearch.group()

        _complIn = str(_wellToCellConnections).split("\n")
        _complOut = convert_completition(_wellname, _complIn)

        _perfData = _perfData + str(_complOut)

    return _perfData


def create_well_perf_table(_date, _wells, _wellNamePattern, _wellToCellConnectionsPattern):

    _perfTable = ""

    for _w in _wells:
        _wellnameSearch = re.search(_wellNamePattern, _w)
        _wellname = _wellnameSearch.group()

        _wellToCellConnectionsSearch = re.search(_wellToCellConnectionsPattern, _w)
        _wellToCellConnections = _wellToCellConnectionsSearch.group()

        _complIn = str(_wellToCellConnections).split("\n")
        _complOut = convert_completition(_wellname, _complIn)

        _perfTable = _perfTable + CreateCompletitionTable(_date, _wellname, _complIn)

    return _perfTable


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


def convert_completition(wellname, perforation):
    #_res = "DATES\n" + _date[0].replace("[(", "").replace("-", " ") + "\n/\n" + "COMPDAT\n"
    _res = "COMPDAT\n"

    for str1 in perforation:
        #_perf = str1.strip().split()
        _perf = re.split('\\s{2,}', str1.strip())

        # 00 = {str}        '(259 120 1)'
        # 01 = {str}        '"Perforation 1"'
        # 02 = {str}        '1'
        # 03 = {str}        'OPEN'
        # 04 = {str}        '8510.5501568949'
        # 05 = {str}        '8875.30787972732'
        # 06 = {str}        '0.3125'
        # 07 = {str}        '0'
        # 08 = {str}        '1'
        # 09 = {str}        '33.1869738095946'
        # 10 = {str}        '12.9647897524728'
        # 11 = {str}        '0.0196803862223565'

        if len(_perf) >= 11 and _perf[0] != "Cell":

            if _perf[6] != "UNCHANGED":
                _state = "OPEN" if _perf[3] == "OPEN" else "SHUT"

                _cells = _perf[0].replace("(", "").replace(")", "").split()
                # _res = _res + "{} {} {} {} {} {} {} {} {} {} {} {} /\n".format(wellname, _perf[0].replace("(", ""), _perf[1], _perf[2].replace(")", ""),
                #                                                         _state, "1*", _perf[14], (2 * float(_perf[9])), _perf[13], _perf[11], "3*", _perf[12])

                _res = _res + "{} {} {} {} {} {} {} {} {} {} {} {} {} / {}\n".format(wellname.replace("WellDef ", ""),
                                                                                  _cells[0], _cells[1], _cells[2], _cells[2],
                                                                                  _state, "1*", _perf[11], (2 * float(_perf[6])),
                                                                                  _perf[10], _perf[7], "3*", _perf[9], _perf[1])

    _res = _res + "/\n\n"
    #print(_res)
    return _res

def CreateCompletitionTable(date, wellname, perforation):
    _res = ""

    for str1 in perforation:
        _perf = re.split('\\s{2,}', str1.strip())
        # 00 = {str}        '(259 120 1)'
        # 01 = {str}        '"Perforation 1"'
        # 02 = {str}        '1'
        # 03 = {str}        'OPEN'
        # 04 = {str}        '8510.5501568949'
        # 05 = {str}        '8875.30787972732'
        # 06 = {str}        '0.3125'
        # 07 = {str}        '0'
        # 08 = {str}        '1'
        # 09 = {str}        '33.1869738095946'
        # 10 = {str}        '12.9647897524728'
        # 11 = {str}        '0.0196803862223565'

        if len(_perf) >= 11: # and _perf[0] != "Cell":
             _res = _res + "{} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(date , wellname.replace("WellDef ", ""),
                                                                                  _perf[0].replace("(", "").replace(")", ""),
                                                                                  _perf[1], _perf[2], _perf[3], _perf[4],
                                                                               _perf[5], _perf[6], _perf[7], _perf[8],
                                                                               _perf[9], _perf[10], _perf[11])

    return _res

if __name__ == '__main__':
    main()
    pass