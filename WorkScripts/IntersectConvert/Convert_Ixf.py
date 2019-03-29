# To get "WellDef" a regex "(WellDef.*(\n(.*|\n)*?}))" is used    DATE.*(\n(.*|\n)*?\s*(?=DATE))

import re

def main():
    #_fileIn = "RM2_HM_PVT_KV_27FEB_WELLS.ixf"
    _fileIn = "RM2_HM_PVT_KV_27FEB_WELL_CONNECTIONS.ixf"
    _buffer = open(_fileIn).read()

    #_wellPattern = re.compile('(WellDef.*{\\n(.*|\\n)*?})', re.MULTILINE) # возвращает tuple
    _wellPattern = re.compile('WellDef.*{(?:\\n(?:.*|\\n)*?})', re.MULTILINE) #в отличае от предыдущего возвращает строки

    #_datePattern = re.compile('DATE.*\\n(.*|\\n)*?.*(?=DATE)')

    _datePattern = re.compile('(\\b\\d{1,2}-+([A-Za-z]){3}-+\\d{1,4})')

    _wellNamePattern = re.compile('WellDef.*"(.*?)"', re.MULTILINE)
    # _headDensityCalculationPattern = re.compile('HeadDensityCalculation=([A-Za-z"]*)', re.MULTILINE)
    # _allowCrossFlowPattern = re.compile('AllowCrossFlow="(.*?)"', re.MULTILINE)
    # _pseudoPressureModelPattern = re.compile('PseudoPressureModel=([A-Za-z"]*)', re.MULTILINE)
    # _frictionPattern = re.compile('Friction="(.*?)"', re.MULTILINE)
    # _accelerationPattern = re.compile('Acceleration="(.*?)"', re.MULTILINE)
    _undefinedPattern = re.compile('Undefined="(.*?)"', re.MULTILINE)

    _wellToCellConnectionsPattern = re.compile('WellToCellConnections.*[[](\\n(.*|\\n)*?\\s*)[]]', re.MULTILINE)

    # _constraintDevicePattern = re.compile('ConstraintDevice.*{(\\n(.*|\\n)*?\\s*)}', re.MULTILINE)
    # _segmentNodesPattern = re.compile('SegmentNodes.*\[(\\n(.*|\\n)*?\\s*)\]', re.MULTILINE)
    # _segmentPipesPattern = re.compile('SegmentPipes.*\[(\\n(.*|\\n)*?\\s*)\]', re.MULTILINE)
    #
    # _resVolConditionsPattern = re.compile('ResVolConditions.*{(\\n(.*|\\n)*?\\s*)}', re.MULTILINE)
    # #_headDensityCalculationPattern = re.compile('HeadDensityCalculation=([A-Za-z]*)', re.MULTILINE)


    #_result1 = _datePattern.match(_buffer)

    #_result = _datePattern.findall(_buffer)

    lines = open(_fileIn, "r").readlines()

    _dates = []
    _substr = ""

    for ln in lines:
        if ln.__contains__("DATE"):
            _dates.append(_substr)
            _substr = ""

        _substr = _substr + ln

    for t1 in _dates:
        _date = _datePattern.findall(t1)

        if len(_date)>0:
            _well = _wellPattern.findall(t1)

            for _w in _well:
                _undef = _undefinedPattern.findall(_w)
                _wellname = _wellNamePattern.findall(_w)
                _wellToCellConnections = _wellToCellConnectionsPattern.findall(_w)

                _compl = str(_wellToCellConnections[0][0]).split("\n")
                ConvertCompletition(_wellname, _compl)

                print(str(_date) + " " + str(_undef)) # + " " + str(_wellToCellConnections))














    #print(_dates)
#    print(_result.group(0))
    #for _w in _result:

        #_date = _datePattern.match(_w)

        # _wellName = _wellNamePattern.findall(_w)
        # _headDensityCalculation= _headDensityCalculationPattern.findall(_w)
        # _allowCrossFlow = _allowCrossFlowPattern.findall(_w)
        # _pseudoPressureModel = _pseudoPressureModelPattern.findall(_w)
        # _friction = _frictionPattern.findall(_w)
        # _acceleration = _accelerationPattern.findall(_w)
        # _undefined = _undefinedPattern.findall(_w)
        #
        # _wellToCellConnections = _wellToCellConnectionsPattern.findall(_w)
        #
        # _constraintDevice = str(_constraintDevicePattern.findall(_w)).replace("\\n","")
        # _segmentNodes = _segmentNodesPattern.findall(_w)
        # _segmentPipes = _segmentPipesPattern.findall(_w)
        #
        # _resVolConditions = _resVolConditionsPattern.findall(_w)
        #
        # line = '{} {} {} {} {} {} {} {} {} {} {} {}'.format(_wellName, _headDensityCalculation, _allowCrossFlow, _pseudoPressureModel, _friction, _acceleration, _undefined, _wellToCellConnections,
        #                                         _constraintDevice, _segmentNodes, _segmentPipes, _resVolConditions)

        #print(_w)

    # with open("models.txt") as f:
    #     lines = f.read().splitlines()
    #
    #     for ln in lines:
    #         s = ln.replace("\t", " ").split(' ', -1)
    #         s1 = s[1].split('/',-1)
    #         s1_upd = ""
    #
    #         for l1 in s1[:-1]:
    #             s1_upd = s1_upd + "\\" +l1
    #
    #         fIn = "Y:\models." + s[0] + s1_upd
    #
    #         CopyModels(fIn, folderOut + "\\" + str(cnt) + "_" + s1[-2])
    #
    #         print("Model " + s1[-1])
    #         cnt+=1

    print("Done.")


def ConvertCompletition(wellname, perforation):

    for str1 in perforation:
        _perf = str1.strip().split()



if __name__ == '__main__':
    main()
    pass