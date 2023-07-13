import xlrd as xl
import glob, os

file = "Book1.xlsx"

# print("Обрабатываю файл {}".format(file))

xl_workbook = xl.open_workbook(filename=file)
# sheet = rb.sheet_by_index(0)  # берем первый лист из экслевской книги

sheet_names = xl_workbook.sheet_names()
#print('Sheet Name: {}'.format(sheet_names))

# for sheet in sheet_names:
#  xl_sheet = xl_workbook.sheet_by_name(sheet)
xl_sheet = xl_workbook.sheet_by_index(0)

for row in range(70,76):
    value = float(xl_sheet.cell_value(rowx=row, colx=3))*62.4279605761446

    print(value)

# #row = xl_sheet.row_values(18)
# #value2 = row[1]
#
# oil_fvf = []
#
# for cell_row in range(148,189):
# #  if xl_sheet.cell_value(cell_row,0) != "":
# #    value = {"pressure" : float(xl_sheet.cell_value(cell_row, 0)), "main_field" : float(xl_sheet.cell_value(cell_row, 2)), "weight" : None}
# #    oil_fvf.append(value)
#   if xl_sheet.cell_type(cell_row, 1) != xl.XL_CELL_EMPTY:
#     print(oil_fvf)