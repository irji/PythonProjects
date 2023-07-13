import re

tables_lk12 = {
    "BB1005H": 434,
    "BB1006H": 435,
    "BB1007H": 436,
    "BB1008H": 437,
    "BB443H": 441,
    "BB455H": 439,
    "BB457H": 419,
    "BB461H": 420,
    "BB465AH": 422,
    "BB465H": 421,
    "BB472H": 423,
    "BB473AH": 425,
    "BB473H": 424,
    "BB474H": 426,
    "BB479H": 427,
    "BB484AH": 429,
    "BB484H": 428,
    "BB488H": 430,
    "BB495H": 431,
    "BB496H": 432,
    "BB504H": 433,
    "BB510H": 442,
    "BB512H": 443,
    "BB513H": 444,
    "BB514H": 445,
    "BB516H": 446,
    "BB517H": 447,
    "BB518H": 440,
    "BB521H": 448,
    "BB536H": 455,
    "BB539H": 449,
    "BB544H": 450,
    "BB595H": 451,
    "BB596H": 452,
    "BB599H": 453,
    "BB610H": 454
}

tables_lk13 = {
    "BB796H": 456,
    "BB839H": 457,
    "BB840H": 458,
    "BB841H": 459,
    "BB841AH": 460,
    "BB842H": 461,
    "BB843H": 462,
    "BB844H": 463,
    "BB846H": 464,
    "BB1129H": 465,
    "BB1133H": 466,
    "BB1127H": 467,
    "BB1128H": 468,
    "BB1241H": 469,
    "BB1233H": 470,
    "BB1234H": 471
}





file_in = "LK13_14_ORI_SCHEDULE.inc"
file_out = "LK13_14_ORI_SCHEDULE_MOD.inc"

_lines = open(file_in, "r").readlines()
flag = False

vfp_table = re.compile('([0-9]+)\s+/')

_resFile = open(file_out, 'w')

tables = tables_lk13

for line in _lines:
    if "WCONPROD" in line:
        flag = True
    if line.startswith("/"):
        flag = False

    if flag:
        line2 = line.replace('1*', '0')
        line2 = line2.replace('2*', '0 0')
        line2 = line2.replace('3*', '0 0 0')
        line2 = line2.replace('4*', '0 0 0 0')
        line2 = line2.replace('5*', '0 0 0 0 0')
        line2 = line2.replace('6*', '0 0 0 0 0 0')

        for wname in tables:
            if wname in line:
                arg_count = line2.split()

                if len(arg_count) != 12:
                    if len(arg_count) != 3:
                        print(line.rstrip())
                else:
                    #line = line.rstrip() + str(tables[wname]) + "\n"
                    line = re.sub('([0-9]+)\s+/', "{}   {}".format(str(tables[wname]),"/"), line)

    _resFile.write(line)
