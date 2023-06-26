# new_wells_data =(
#     ("Prod1",4000,1),
#     ("Prod1",8000,2),
#     ("Prod2",6000,3),
#     ("Prod2",9000,4),
#     ("Prod2",19000,5)
# )
# # #==================
# # well = "Prod1"
# # prod_value = 7500
# # #==================
# #
# # mult_value = 1
# #
# # for k in new_wells_data:
# #     if k[0] == well:
# #         if prod_value > k[1]:
# #             mult_value = k[2]
# #
# # print(mult_value)
#
# mult_value = 1
#
# print(mult_value)


# import pandas as pd
#
# data = pd.read_excel('D:\Models\Luna\GDC.xlsx', index_col=0)
#
# print(data)


import math

a = math.sin(math.radians(30))

print(a)


def func1():
    POOL = 0.
    SHRINK = 0.
    FUEL = 0.
    SALES = 0.
    MAKEUP = 0.

    gr = get_group_by_name('GAS-TRN_PROD_BH_GROUP')

    QPROD = ggpr[gr]

    MAKEUP = MAKEUP + 0. * QPROD
    QG1 = POOL + SHRINK + FUEL + SALES - QPROD

    if POOL > 0 and QG1 > 0:
        POOL = POOL * 0.75
        #    SET_TARGET("VALUE", VOIDAGE_INJGA2, POOL)
        set_group_inj_limit(group="GAS-TRN_GasReinjSurf_Group", control_mode='rate', rein_frac=POOL)
        print("Reinjection fraction = {}".format(POOL))
    else:
        #QAVAIL = MAX(0, QPROD - SHRINK)
        QAVAIL = 0 if QPROD - SHRINK < 0 else QPROD - SHRINK
        POOL = FUEL + SALES
        if POOL > QAVAIL:
            POOL = POOL - QAVAIL
            if MAKEUP > POOL:
                MAKEUP = MAKEUP - POOL
                POOL = POOL + QAVAIL
            else:
                POOL = MAKEUP + QAVAIL
                MAKEUP = 0

            #QAVAIL = MAX(0, QAVAIL - POOL)
            QAVAIL = 0 if QPROD - SHRINK < 0 else QAVAIL - POOL
        else:
            QAVAIL = QAVAIL - POOL

    QAVAIL = QAVAIL + MAKEUP
    QAVAIL = QAVAIL * 0.75
    set_group_inj_limit(group="GAS-TRN_GasReinjSurf_Group", control_mode='rate', rein_frac=QAVAIL)

