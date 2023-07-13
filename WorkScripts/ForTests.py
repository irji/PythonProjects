# rb = xl.open_workbook(folder + '2027_Беркет-Ключевское_замеры_1520м.xls', formatting_info=True)
from datetime import datetime

first_event_well_names = {
    'LA501': '01.08.2027',
    'LA502': '01.06.2026',
    'LA503': '01.11.2021',
    'LA506': '01.02.2024',
    'LA507': '01.12.2022',
    'LA511': '01.07.2019',
    'LA513ST2': '01.03.2025',
    'LA517': '01.09.2020',
    'LA521': '01.09.2028'
}

for well in first_event_well_names:
  #date = datetime.strftime(str(first_event_well_names[well]), '%d.%m.%Y')
  date = first_event_well_names[well]
  dt = datetime.strptime(first_event_well_names[well], '%d.%m.%Y')
  print(date)












# import xlrd as xl
# import glob, os
#
# folder = "D:/Scripts/Python_Excel/"
# files = {}
# result_file = "well.txt"
#
# ##### Ищем файл с максимальным значением глубины в конце названия
# for file in os.listdir(folder):
#     if file.endswith(".xls"):
#         ####=========================================================================================
#         name = file.replace(".xls", "").split("_") # убираем из имени файла расширение и разбиваем имя на элементы по '_'
#         files.update({int(name[-1].replace("м", "")): file})
# last_val = max(files.keys())
#
# print("Обрабатываю файл {}".format(files.get(last_val)))
#
# rb = xl.open_workbook(folder + files.get(last_val))
# sheet = rb.sheet_by_index(0)  # берем первый лист из экслевской книги
#
# well_name = str(sheet.row_values(4)[1])  # получаем номер скважины из ячейки B5 (номера строк и столбцов начинаются с 0, а не с 1 как в экселе)
#
# depth = 0
# incl = 0
# azim = 0
#
# with open(well_name + '.txt', 'w') as the_file:
#     for rownum in range(7, sheet.nrows):
#         row = sheet.row_values(rownum)
#         if row[1] != "":
#             depth = row[1] # Колонка "Глубина по датчику, м"
#         if row[2] != "":
#             incl = row[2] # Колонка "Зенитный  угол, град"
#         if row[3] != "":
#             azim = row[3] # Колонка "Азимут истинный, град"
#
#         the_file.write("{} {} {}\n".format(depth, incl, azim))
#     #    print(well_name + "  " + str(depth) + "  " + str(incl) + "  " + str(azim))





#  for cell in row:
#     print(cell)


# print(sheet.name)


# import os
# import numpy as np
#
# dx = 42
# dy = 74
# dz = 150
#
# # x1 = np.array(466200 * [0])
# # x2 = np.zeros(466200)
#
# x1 = np.array(dy * [np.zeros(dx)])
# x3 = np.array(dz * [x1])
#
# # x1 = np.array( [42 * [0], 74 * [0]])
# inFile = "D:/Work/Models/Designer/Rus/Siec/Astoh/01_Astokh/Appendixes/Appendix2_Static_input/02_Export_from_MoReS/ECL.NNC"
#
# with open(inFile) as fl:
#     lines = fl.read().splitlines()
#
#     for ln in lines:
#         if ln.lstrip().find("NNC") == -1:
#             coord = ln.lstrip().split()
#             if len(coord) > 0:
#                 if coord[0].isdigit() == True:
#                     #print("Cell {} {} {}".format(coord[0], coord[1], coord[2]))
#                     #index = int(coord[0]) * int(coord[1]) * int(coord[2])
#                     c1 = int(coord[0]) - 1
#                     c2 = int(coord[1]) - 1
#                     c3 = int(coord[2]) - 1
#
#                     c4 = int(coord[3]) - 1
#                     c5 = int(coord[4]) - 1
#                     c6 = int(coord[5]) - 1
#
#                     x3[c3][c2][c1] = 1
#                     x3[c6][c5][c4] = 1
#
#                     #index = int(coord[3]) * int(coord[4]) * int(coord[5])
#                     #x3[index] = 1
# #          print("Cell {} {} {}".format(coord[0], coord[1], coord[2]))
#
# #x3 = x3.reshape(150,dx*dy)
# x3 = x3.ravel()
# np.savetxt("Prop1.txt", (x3), newline="\n", header="Prop1", footer="/")
#
# # print(x3)










def __init_script__ ():
  create_graph (name = 'gas_flare', type = 'field', default_value = 0, export = True, units = 'metric')

def eos_rein():
 add_keyword(
 """
 WTAKEGAS SFR /
 /
 """
 )

 if fgpr<=30000:
   if is_report_step():
    C2H6_separation=0.983
    C3H8_separation=0.998
    C4H10_separation=0.999
    C5H12_separation=0.999
    C10H22_separation=1
    print (str(C2H6_separation))
    print (str(C3H8_separation))
    print (str(C4H10_separation))
    print (str(C5H12_separation))
    print (str(C10H22_separation))
    add_keyword(
    """
    GRUPSALE
    FIELD 0 1  1 1 1 0 0 0 """+str(C2H6_separation)+""" """+str(C3H8_separation)+""" """+str(C4H10_separation)+""" """+str(C5H12_separation)+""" """+str(C10H22_separation)+""" /
    /
    """
    )
    add_keyword(
    """
    GINJGAS FIELD GV /
    /
    """
    )
    add_keyword(
    """
    GCONINJE FIELD GAS REIN /
    /
    """
    )
   if fgpr>30000:
    if is_report_step():
     C2H6_separation=0.983*(30000/fgpr)
     C3H8_separation=0.998*(30000/fgpr)
     C4H10_separation=0.999*(30000/fgpr)
     C5H12_separation=0.999*(30000/fgpr)
     C10H22_separation=1*(30000/fgpr)
     print (str(C2H6_separation))
     print (str(C3H8_separation))
     print (str(C4H10_separation))
     print (str(C5H12_separation))
     print (str(C10H22_separation))
     add_keyword(
     """
     GRUPSALE
     FIELD 0 1  1 1 1 0 0 0 """+str(C2H6_separation)+""" """+str(C3H8_separation)+""" """+str(C4H10_separation)+""" """+str(C5H12_separation)+""" """+str(C10H22_separation)+""" /
     /
     """
     )
     add_keyword(
     """
     WELLSTRE 'STREAM_1' 0 0 0 1 1 1 """+str(1-C2H6_separation)+""""""+str(1-C3H8_separation)+""" """+str(1-C4H10_separation)+""" """+str(1-C5H12_separation)+""" """+str(1-C10H22_separation)+""" /
     /
     """
     )
     add_keyword(
     """
     GINJGAS FIELD GV FIELD 'STREAM_1' /
     /
     """
     )
     a = (fgpr-ggsr) + (fgpr-30000)
     if a <= 50000:
      add_keyword(
      """
      GCONINJE FIELD GAS RATE """+str(a)+""" /
      /
      """
      )
      else:
      add_keyword(
      """
      GCONINJE FIELD GAS RATE 50000 /
      /
      """
      )
 if b > fgir:
   gas_flare = b-fgir
   export(gas_flare, name = 'gas_flare')
