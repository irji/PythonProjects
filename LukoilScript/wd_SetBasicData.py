import pandas as pd
import numpy as np

# Путь до excel фала, названия листов с которых данные читаем
fileIn = "D:\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
well_names_list = "WellList"
equipment_data_list = "EquipmentData"

# Чтение из excel листов / убираем пустые строки
well_basic_data = pd.read_excel(fileIn, sheet_name=well_names_list, header=0, skiprows=5)
well_basic_data.dropna(subset=["Well"], inplace=True)

equipment_data = pd.read_excel(fileIn, sheet_name=equipment_data_list, header=0, skiprows=5)
equipment_data.dropna(subset=["Well"], inplace=True)

############################################
equip_row_value = equipment_data.loc[equipment_data["Well"] == "W_SHR_220_BB"]
wlist_row_value = well_basic_data.loc[well_basic_data["Well"] == "W_SHR_220_BB"]
############################################

x1 = wlist_row_value["SystemType"].values[0]
# print(x1)
#
# if wlist_row_value["SystemType"].values[0] == "PRODUCTION":
#     print("Hi1")

label_value = equip_row_value["Label.1"].values[0][:-1].split("|")
type_value = equip_row_value["Type.1"].values[0][:-1].split("|")
md_value = equip_row_value["Measured Depth, feet"].values[0][:-1].split("|")
tub_in_d_value = equip_row_value["Tubing Inside Diameter, inches"].values[0][:-1].split("|")
tub_out_d_value = equip_row_value["Tubing Outside Diameter, inches"].values[0][:-1].split("|")
casing_in_d_value = equip_row_value["Casing Inside Diameter, inches"].values[0][:-1].split("|")
tub_in_roughness_value = equip_row_value["Tubing Inside Roughness, inches"].values[0][:-1].split("|")
tub_out_roughness_value = equip_row_value["Tubing Outside Roughness, inches"].values[0][:-1].split("|")
casing_in_roughness_value = equip_row_value["Casing Inside Roughness, inches"].values[0][:-1].split("|")

downhole_equipment_data = { "Lable": label_value, "Type": type_value, "MD": md_value, "Tub_in_D": tub_in_d_value, "Tub_in_rough": tub_in_roughness_value,
                            "Tub_out_D": tub_out_d_value, "Tub_out_rough": tub_out_roughness_value, "Casing_in_D": casing_in_d_value, "Casing_in_rough": casing_in_roughness_value }
df_downhole_equipment_data = pd.DataFrame(downhole_equipment_data)


print(x1)