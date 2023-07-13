import plotly







# import os
#
# inFile = "D:/Work/Models/Simulator/UAE/ModelConvert/Nexus/Lower-Zakum/Dynamic_Nexus/IV_DYNAMIC_MODEL/IV_HIST&MTDP&EPS/2019/00_HIST/THIV_REF_HIST_DEC18.out"
#
# with open(inFile, 'r') as fl:
#     lines = fl.read().splitlines()
#
#     for line in lines:
#         if 'DAY/MO/YR' in line:
#              print(line)
#
#         #if line.find('Elapsed time') != -1:
#         #print(line)
#
#     #print(str(lines[1244220]))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # # rb = xl.open_workbook(folder + '2027_Беркет-Ключевское_замеры_1520м.xls', formatting_info=True)
# #
# #
# # import xlrd as xl
# # import glob, os
# #
# # folder = "D:/Scripts/Python_Excel/"
# # files = {}
# # result_file = "well.txt"
# #
# # ##### Ищем файл с максимальным значением глубины в конце названия
# # for file in os.listdir(folder):
# #     if file.endswith(".xls"):
# #         ####=========================================================================================
# #         name = file.replace(".xls", "").split("_") # убираем из имени файла расширение и разбиваем имя на элементы по '_'
# #         files.update({int(name[-1].replace("м", "")): file})
# # last_val = max(files.keys())
# #
# # print("Обрабатываю файл {}".format(files.get(last_val)))
# #
# # rb = xl.open_workbook(folder + files.get(last_val))
# # sheet = rb.sheet_by_index(0)  # берем первый лист из экслевской книги
# #
# # well_name = str(sheet.row_values(4)[1])  # получаем номер скважины из ячейки B5 (номера строк и столбцов начинаются с 0, а не с 1 как в экселе)
# #
# # depth = 0
# # incl = 0
# # azim = 0
# #
# # with open(well_name + '.txt', 'w') as the_file:
# #     for rownum in range(7, sheet.nrows):
# #         row = sheet.row_values(rownum)
# #         if row[1] != "":
# #             depth = row[1] # Колонка "Глубина по датчику, м"
# #         if row[2] != "":
# #             incl = row[2] # Колонка "Зенитный  угол, град"
# #         if row[3] != "":
# #             azim = row[3] # Колонка "Азимут истинный, град"
# #
# #         the_file.write("{} {} {}\n".format(depth, incl, azim))
# #     #    print(well_name + "  " + str(depth) + "  " + str(incl) + "  " + str(azim))
# #
#
#
#
#
# # import os
# # import numpy as np
# #
# # dx = 42
# # dy = 74
# # dz = 150
# #
# # # x1 = np.array(466200 * [0])
# # # x2 = np.zeros(466200)
# #
# # x1 = np.array(dy * [np.zeros(dx)])
# # x3 = np.array(dz * [x1])
# #
# # # x1 = np.array( [42 * [0], 74 * [0]])
# # inFile = "D:/Work/Models/Designer/Rus/Siec/Astoh/01_Astokh/Appendixes/Appendix2_Static_input/02_Export_from_MoReS/ECL.NNC"
# #
# # with open(inFile) as fl:
# #     lines = fl.read().splitlines()
# #
# #     for ln in lines[5:]:
# #         if ln.lstrip().find("NNC") == -1:
# #             coord = ln.lstrip().split()
# #             if len(coord) > 0:
# #                 if coord[0].isdigit() == True:
# #                     #print("Cell {} {} {}".format(coord[0], coord[1], coord[2]))
# #                     #index = int(coord[0]) * int(coord[1]) * int(coord[2])
# #                     c1 = int(coord[0]) - 1
# #                     c2 = int(coord[1]) - 1
# #                     c3 = int(coord[2]) - 1
# #
# #                     c4 = int(coord[3]) - 1
# #                     c5 = int(coord[4]) - 1
# #                     c6 = int(coord[5]) - 1
# #
# #                     x3[c3][c2][c1] = 1
# #                     x3[c6][c5][c4] = 1
# #
# #                     #index = int(coord[3]) * int(coord[4]) * int(coord[5])
# #                     #x3[index] = 1
# # #          print("Cell {} {} {}".format(coord[0], coord[1], coord[2]))
# #
# # #x3 = x3.reshape(150,dx*dy)
# # x3 = x3.ravel()
# # np.savetxt("Prop1.txt", (x3), newline="\n", header="Prop1", footer="/")
# #
# # # print(x3)
