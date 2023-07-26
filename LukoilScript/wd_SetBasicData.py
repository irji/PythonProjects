import pandas as pd
import numpy as np

##################  FOR DEBUG  #########################################

# Чтение данных с указанного листа из excel
def excel_row_reader(well_name: str, column_name: str, list_name: str, srip_rows: int):
    # Чтение из excel листов / убираем пустые строки
    try:
        data_from_list = pd.read_excel(fileIn, sheet_name=list_name, header=0, skiprows=srip_rows)
        data_from_list.dropna(subset=[column_name], inplace=True)

        data_from_list["Well"] = data_from_list["Well"].fillna(method='ffill')
        row_values = data_from_list.loc[data_from_list["Well"] == well_name]
    except:
        raise SystemError("Невозможно получить данные из excel файла!")
        #print_log(text="Невозможно получить данные из excel файла!", severity="error")

    # Проверяем на ошибки
    if len(row_values) == 0:
        raise SystemError("Нет данных для скважины '{}' в excel файле!".format(well_name))
        #print_log(text="Нет данных для скважины '{}' в excel файле!".format(well_name), severity="error")

    return row_values

# Читаем данные из dataframe и конвертируем в числа.
# Возвращаем массив чисел в метрической системе или как есть в зависимости от значения units.
def data_reader(column_name: str, units: str, df: pd.DataFrame, well_name: str):
    df_out = np.array([])

    try:
        value = str(df[column_name].values[0]).strip().rstrip("|")

        if pd.isna(df[column_name].values[0]) != True:
            if len(value.split("|")) > 1:
                df_out = value.split("|")
            else:
                df_out = value
        else:
            df_out = np.array([])
    except:
        df_out = np.array([])

    try:
        if units == "feet":
            df_out = np.array(df_out, dtype="float") * 0.3048  # Конвертируем feet в метры
        if units == "inches":
            df_out = np.array(df_out, dtype="float") * 0.0254  # Конвертируем inches в метры
        if units == "F":
            df_out = (np.array(df_out, dtype="float") - 32)/1.8 # Конвертируем F в C
        if units == "psig":
            df_out = np.array(df_out, dtype="float") * 0.0689475728 # Конвертируем psig в bar
        if units == "%":
            df_out = np.array(df_out, dtype="float") * 0.01 # Конвертируем % в д.е.
        if units == "STB/day":
            df_out = np.array(df_out, dtype="float") * 0.158987  # Конвертируем STB/day в sm3/day.
        if units == "scf/STB":
            df_out = np.array(df_out, dtype="float") * 0.1781076  # Конвертируем scf/STB в sm3/sm3.
        if units == "date":
            df_out = np.array(pd.to_datetime(df_out, format="%d/%m/%Y"))   # Конвертируем строки в даты.
        if units == "btu":
            df_out = np.array(df_out, dtype="float") * 4.1863  # Конвертируем BTU/lb/F в kJ/kg∙K.
        if units == "STB/day/psi":
            df_out = np.array(df_out, dtype="float") * 0.433667  # Конвертируем STB/day/psi в sm3/day/bar.
        if units == "btu/h/ft2/F":
            df_out = np.array(df_out, dtype="float") * 5.67826334  # Конвертируем btu/h/ft2/F в J/sec/C/m2.
        if units == "RB/day":
            df_out = np.array(df_out, dtype="float") * 0.15898729  # Конвертируем RB/day в m3/day.
        if units == "number":
            df_out = np.array(df_out, dtype="float") * 1 # Возвращаем числа или массив чисел без конвертации
        if units == "":
            df_out = df_out # Возвращаем значения как есть
    except Exception:
        print("Ошибка при работе с скважиной {}".format(well_name))
        # print_log(text="Ошибка при работе с скважиной {}".format(well_name), severity="warning")

    return df_out


##################  FOR DEBUG  #########################################

fileIn = "D:\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
#fileIn = "D:\Work\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"

well_names_list = "WellList"
equipment_data_list = "EquipmentData"
summary_data_list = "SummaryData"
vlp_data_list = "VLPIPRData"
ipr_data_list = "IPRData"
esp_data_list = "DataBase"

ipr_phase = "liquid"
well_type = "producer"

current_well_name = "W_SHR_69_BB_I"

##################  FOR DEBUG  #########################################


#current_well_name = get_project_name ()

# Выставляем для выбранной скважины ее тип и предпочитаемый тип флюида
def set_well_basic_data(name: str, well_row: pd.DataFrame):
    well_type = "producer"
    phase = "LIQ"

    name_param = str(name).split("_")

    # Поддержано типы PRODUCTION/WATERINJECTION
    if well_row["Well Type"].values[0] == 2: #"WATERINJECTION":
        well_type = "injector"
        phase = "WATER"

    # if well_row["Well Type"].values[0] == "2": #"GASINJECTION":
    #      well_type = "injector"
    #      phase = "GAS"
    #      ipr_phase = "gas"

    well_designer_adjust_basic_data(name=name_param[2],
                                    group_name="", object="well", well_type=well_type,
                                    current_vfp="", preferred_phase=phase,
                                    inflow_equation="STD", instructions="SHUT", density_type="SEG", drainage_radius=0,
                                    crossflow_ability=True, max_deviation_angle=5, use_segment_model=False,
                                    flow_model=False, use_segment_params=False, min_segment_length=0, max_segment_length=1000,
                                    well_head_x=VAR_X,
                                    well_head_y=VAR_Y,
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

print("Чтение основных данных для скважины {}.".format(current_well_name))

equip_row_value = excel_row_reader(current_well_name, "Well", equipment_data_list, 5)
wlist_row_value = excel_row_reader(current_well_name, "Well", well_names_list, 5)
summary_row_value = excel_row_reader(current_well_name, "Well", summary_data_list, 5)

####### Задаем basic data ####################################################
set_well_basic_data(current_well_name, summary_row_value)

####### Читаем конструкцию ###################################################
# Берем данные из колонок с 19 по 27 с листа 'equipment_data_list'
label_value = equip_row_value["Label.1"].values[0][:-1].split("|")
type_value = equip_row_value["Type.1"].values[0][:-1].split("|")
# label_value = data_reader("Label.1", "", equip_row_value, current_well_name)
# type_value = data_reader("Type.1", "", equip_row_value, current_well_name)

md_value = data_reader("Measured Depth, feet", "feet", equip_row_value, current_well_name)
tub_in_d_value = data_reader("Tubing Inside Diameter, inches", "inches", equip_row_value, current_well_name)
tub_out_d_value = data_reader("Tubing Outside Diameter, inches", "inches", equip_row_value, current_well_name)
casing_in_d_value = data_reader("Casing Inside Diameter, inches", "inches", equip_row_value, current_well_name)
tub_in_roughness_value = data_reader("Tubing Inside Roughness, inches", "inches", equip_row_value, current_well_name)
tub_out_roughness_value = data_reader("Tubing Outside Roughness, inches", "inches", equip_row_value, current_well_name)
casing_in_roughness_value = data_reader("Casing Inside Roughness, inches", "inches", equip_row_value, current_well_name)

# type:
# 1 - Tubing; # 2 - SSSV; # 3 - Restriction; # 4 - Casing

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
