import pandas as pd
import numpy as np

# Читаем данные из dataframe и конвертируем в числа.
# Возвращаем массив чисел в метрической системе или как есть в зависимости от значения units.
def read_data(name: str, units: str, df: pd.DataFrame):
    conv_inches_metric = 0.0254
    conv_feet_metric = 0.3048

    df_out = df[name].values[0][:-1].split("|")

    if units == "feet":
        df_out = np.array(df_out, dtype="float") * conv_feet_metric  # Конвертируем feet в метры
    if units == "inches":
        df_out = np.array(df_out, dtype="float") * conv_inches_metric  # Конвертируем inches в метры
    if units == "":
        df_out = np.array(df_out, dtype="float")

    return df_out




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

# Берем данные из колонок с 19 по 27
label_value = equip_row_value["Label.1"].values[0][:-1].split("|")
type_value = equip_row_value["Type.1"].values[0][:-1].split("|")

md_value = read_data("Measured Depth, feet", "feet", equip_row_value)
tub_in_d_value = read_data("Tubing Inside Diameter, inches", "inches", equip_row_value)
tub_out_d_value = read_data("Tubing Outside Diameter, inches", "inches", equip_row_value)
casing_in_d_value = read_data("Casing Inside Diameter, inches", "inches", equip_row_value)
tub_in_roughness_value = read_data("Tubing Inside Roughness, inches", "inches", equip_row_value)
tub_out_roughness_value = read_data("Tubing Outside Roughness, inches", "inches", equip_row_value)
casing_in_roughness_value = read_data("Casing Inside Roughness, inches", "inches", equip_row_value)

# type:
# 1 - Tubing
# 2 - SSSV
# 3 - Restriction
# 4 - Casing

downhole_equipment_data = {"Lable": label_value, "Type": type_value, "MD": md_value, "Tub_in_D": tub_in_d_value,
                           "Tub_in_rough": tub_in_roughness_value,
                           "Tub_out_D": tub_out_d_value, "Tub_out_rough": tub_out_roughness_value,
                           "Casing_in_D": casing_in_d_value, "Casing_in_rough": casing_in_roughness_value}
df_downhole_equipment_data = pd.DataFrame(downhole_equipment_data)

# df_tubing = df_downhole_equipment_data[df_downhole_equipment_data['Tub_in_D'] != 0]
# df_casing = df_downhole_equipment_data[df_downhole_equipment_data['Casing_in_D'] != 0]

df_tubing = df_downhole_equipment_data[df_downhole_equipment_data['Type'] != 1]
df_casing = df_downhole_equipment_data[df_downhole_equipment_data['Type'] != 4]

print(x1)
