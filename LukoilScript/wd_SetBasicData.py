import pandas as pd
import numpy as np

def excel_list_reader(well_name: str, list_name: str, srip_rows: int):
    # Чтение из excel листов / убираем пустые строки
    try:
        data_from_list = pd.read_excel(fileIn, sheet_name=list_name, header=0, skiprows=srip_rows)
        data_from_list.dropna(subset=["Well"], inplace=True)

        row_value = data_from_list.loc[data_from_list["Well"] == well_name]
    except:
        raise SystemExit("Unable to get data from excel file!")

    # # Проверяем на ошибки
    if len(row_value) == 0:
        raise SystemExit("There is no data for well with name '{}' in excel file!".format(well_name))

    return row_value


# Читаем данные из dataframe и конвертируем в числа.
# Возвращаем массив чисел в метрической системе или как есть в зависимости от значения units.
def data_reader(name: str, units: str, df: pd.DataFrame):
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

# Выставляем для выбранной скважины ее тип и предпочитаемый тип флюида
def set_well_basic_data(name: str, well_row: pd.DataFrame):
    well_type = "producer"
    phase = "LIQ"

    # Поддержано только два типа (PRODUCTION/WATERINJECTION).
    # TODO: добавить остальные возможные типы
    if wlist_row_value["SystemType"].values[0] == "WATERINJECTION":
        well_type = "injector"
        phase = "WATER"

    # if wlist_row_value["SystemType"].values[0] == "GASINJECTION":
    #      well_type = "injector"
    #      phase = "GAS"

    well_designer_adjust_basic_data(name=name,
                                    group_name="",
                                    object="well",
                                    well_type=well_type,
                                    current_vfp="",
                                    preferred_phase=phase,
                                    inflow_equation="STD",
                                    instructions="SHUT",
                                    density_type="SEG",
                                    drainage_radius=0,
                                    crossflow_ability=True,
                                    max_deviation_angle=5,
                                    use_segment_model=False,
                                    flow_model=False,
                                    use_segment_params=False,
                                    min_segment_length=0,
                                    max_segment_length=1000,
                                    well_head_x=0,
                                    well_head_y=0,
                                    well_head_z=TVD_VAR)

def add_casing(casing_data: pd.DataFrame):
    indx=0

    for index, line in casing_data.iterrows():
        indx += 1

        if line["Casing_in_D"] == 0:
            line["Casing_in_D"] = 0.1158

        well_designer_object_casing(branch_num=0, objects_table=[
            {"name": "Casing_" + str(indx), "top_depth": 0, "bottom_depth": line["MD"], "diameter_in": line["Casing_in_D"],
             "diameter_out": line["Casing_in_D"] + 0.1, "roughness_in": line["Casing_in_rough"], "openhole": False, "liner": False,
             "wall_thermal_capacity": 0, "wall_thermal_conductivity": 0,
             "wellbore_diameter": line["Casing_in_D"] + 0.1, "cement_thermal_conductivity": 0}])

def add_tubing(tubing_data: pd.DataFrame):
    indx=0

    for index, line in tubing_data.iterrows():
        indx += 1

        if line["Tub_in_D"] == 0:
            line["Tub_in_D"] = 0.075

        if line["Tub_out_D"] == 0:
            line["Tub_out_D"] = line["Tub_in_D"] + 0.0139

        well_designer_object_tubing(branch_num=0, objects_table=[
                {"name": "Tubing_" + str(indx), "bottom_depth": line["MD"], "diameter_in": line["Tub_in_D"], "diameter_out": line["Tub_out_D"],
                 "roughness_in": line["Tub_in_rough"], "roughness_out": line["Tub_out_rough"], "bull_plug": False,
                 "wall_thermal_capacity": 0, "wall_thermal_conductivity": 0,
                 "annulus_material_thermal_conductivity": 0}])


########################################################################################################################


# Путь до excel фала, названия листов с которых данные читаем
fileIn = "D:\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
#fileIn = "D:\Work\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
well_names_list = "WellList"
equipment_data_list = "EquipmentData"

current_well_name = "W_SHR_64_BB"
#current_well_name = get_project_name ()


# # Чтение из excel листов / убираем пустые строки
# try:
#     well_basic_data = pd.read_excel(fileIn, sheet_name=well_names_list, header=0, skiprows=5)
#     well_basic_data.dropna(subset=["Well"], inplace=True)
#
#     equipment_data = pd.read_excel(fileIn, sheet_name=equipment_data_list, header=0, skiprows=5)
#     equipment_data.dropna(subset=["Well"], inplace=True)
#
#     ############################################
#     equip_row_value = equipment_data.loc[equipment_data["Well"] == current_well_name]
#     wlist_row_value = well_basic_data.loc[well_basic_data["Well"] == current_well_name]
#     ############################################
# except:
#     raise SystemExit("Unable to get data from excel file!")
#
# # Проверяем на ошибки
# if len(wlist_row_value) == 0:
#     raise SystemExit("There is no well with name '{}' in excel file!".format(current_well_name))
#
# if len(equip_row_value) == 0:
#     raise SystemExit("There is no data for well with name '{}' in excel file!".format(current_well_name))

equip_row_value = excel_list_reader(current_well_name, equipment_data_list, 5)
wlist_row_value = excel_list_reader(current_well_name, well_names_list, 5)

# Задаем basic data
#set_well_basic_data(current_well_name, wlist_row_value)

# Читаем конструкцию
# Берем данные из колонок с 19 по 27 с листа 'equipment_data_list'
label_value = equip_row_value["Label.1"].values[0][:-1].split("|")
type_value = equip_row_value["Type.1"].values[0][:-1].split("|")

md_value = data_reader("Measured Depth, feet", "feet", equip_row_value)
tub_in_d_value = data_reader("Tubing Inside Diameter, inches", "inches", equip_row_value)
tub_out_d_value = data_reader("Tubing Outside Diameter, inches", "inches", equip_row_value)
casing_in_d_value = data_reader("Casing Inside Diameter, inches", "inches", equip_row_value)
tub_in_roughness_value = data_reader("Tubing Inside Roughness, inches", "inches", equip_row_value)
tub_out_roughness_value = data_reader("Tubing Outside Roughness, inches", "inches", equip_row_value)
casing_in_roughness_value = data_reader("Casing Inside Roughness, inches", "inches", equip_row_value)

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

# Данные для Tubing
df_tubing = df_downhole_equipment_data[df_downhole_equipment_data['Type'] == "1"]
# Данные для Casing
df_casing = df_downhole_equipment_data[df_downhole_equipment_data['Type'] == "4"]

# Создаем casing и tubing
add_casing(df_casing)
add_tubing(df_tubing)

print("END_well_type")
