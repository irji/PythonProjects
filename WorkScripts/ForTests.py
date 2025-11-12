COUNT = 1
LGR_COUNT = 70000
LGR_SET = []

for ni in range(1,49):
    for nj in range(1,51):
        for nk in range(1,31):
            if COUNT <= LGR_COUNT:
                LGR_SET.append({"parent_lgr_name" : "", "lgr_name" : "L" + str(COUNT), "i1" : int(ni), "i2" : int(ni),
                                "j1" : int(nj), "j2" : int(nj), "k1" : int(nk), "k2" : int(nk), "ni" : 2, "nj" : 2, "nk" : 1,
                                "log_power" : 0.5, "log_ni" : False, "log_ni_center" : 0, "log_nj" : False, "log_nj_center" : 0,
                                "log_nk" : False, "log_nk_center" : 0, "symmetrical_refinement" : False})


                COUNT = COUNT + 1

print(LGR_SET)

with open("res_upd.txt", "w") as file_out:
    for line in LGR_SET:
        file_out.write(str(line))