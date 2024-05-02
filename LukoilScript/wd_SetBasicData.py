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
            # in_array, min, max
            # Значения меньше 1,01 заменяем на 1,01
            df_out = np.clip(df_out, 1.01325, None)

            # Заменяем значения больше 1e20 на 0
            #if not hasattr(df_out, "__len__"): # число или массив
            if df_out.size == 1:
                if df_out > 1e20:
                    df_out = 0.0
            else:
                df_out[df_out > 1e20] = 0
        if units == "%":
            df_out = np.array(df_out, dtype="float") * 0.01 # Конвертируем % в д.е.
        if units == "STB/day":
            df_out = np.array(df_out, dtype="float") * 0.158987  # Конвертируем STB/day в sm3/day.
        if units == "scf/STB":
            df_out = np.array(df_out, dtype="float") * 0.1781076  # Конвертируем scf/STB в sm3/sm3.
            # Заменяем значения больше 1e20 на 0
            if df_out.size == 1: # число или массив
                if df_out > 1e20:
                    df_out = 0.0
            else:
                df_out[df_out > 1e20] = 0
        if units == "date":
            df_out = np.array(pd.to_datetime(df_out, format="%d/%m/%Y"))   # Конвертируем строки в даты.
        if units == "btu":
            df_out = np.array(df_out, dtype="float") * 4.1863  # Конвертируем BTU/lb/F в kJ/kg∙K.
        if units == "STB/day/psi":
            df_out = np.array(df_out, dtype="float") * 2.305911485  # Конвертируем STB/day/psi в sm3/day/bar.
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

# Убираем все значения из массивов после того как значения перестали уменьшаться
def esp_cut_relation(x_axis: np.ndarray, y_axis: np.ndarray, efficiency_axis: pd.DataFrame, power_axis: pd.DataFrame):
    min_val = np.min(y_axis)

    if min_val < 0:
        for index, elem in np.ndenumerate(y_axis):
            if elem < 0:
                x_axis = x_axis[:index[0]]
                y_axis = y_axis[:index[0]]
                efficiency_axis = efficiency_axis[:index[0]]
                power_axis = power_axis[:index[0]]
                break
    else:
        fliped_HeadY_value = np.flip(y_axis)

        ref_value = fliped_HeadY_value[0]

        for index, elem in np.ndenumerate(fliped_HeadY_value):
            if elem > ref_value:
                y_axis = np.flip(fliped_HeadY_value[index[0] - 1:])
                x_axis = x_axis[:len(y_axis)]
                efficiency_axis = efficiency_axis[:len(y_axis)]
                power_axis = power_axis[:len(y_axis)]
                break
            else:
                ref_value = elem

    # Формируем массив с данными по измерениям
    sample_data = {"rate": x_axis, "head": y_axis, "efficiency": efficiency_axis, "power": power_axis}
    df_sample_data = pd.DataFrame(sample_data)
    df_sample_data = df_sample_data.to_dict('records')

    return df_sample_data

##################  FOR DEBUG  #########################################

#fileIn = "D:\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
fileIn = "D:\Work\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"

well_names_list = "WellList"
equipment_data_list = "EquipmentData"
summary_data_list = "SummaryData"
vlp_data_list = "VLPIPRData"
ipr_data_list = "IPRData"
esp_data_list = "DataBase"

ipr_phase = "liquid"
well_type = "producer"

well_name_in_excel = "W_SHR_220_BB"
well_name = "220_BB"

##################  FOR DEBUG  #########################################

# Выставляем для выбранной скважины ее тип и предпочитаемый тип флюида
def set_well_basic_data(name: str, well_row: pd.DataFrame):
    well_type = "producer"
    phase = "LIQ"

    # Поддержано типы PRODUCTION/WATERINJECTION
    if well_row["Well Type"].values[0] == 2: #"WATERINJECTION":
        well_type = "injector"
        phase = "WATER"

    # if well_row["Well Type"].values[0] == "2": #"GASINJECTION":
    #      well_type = "injector"
    #      phase = "GAS"
    #      ipr_phase = "gas"

    well_designer_adjust_basic_data(name=name,
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
        bot_depth = line["MD"]

        if indx == casing_data.shape[0]:
            well_designer_object_bottom_hole(branch_num=0, objects_table=[
                {"name": "BH_" + str(indx), "depth": bot_depth, "status": "active", "tvd": None, "ref_tvd": None}])

            bot_depth = LAST_MD

        if line["Casing_in_D"] == 0:
            line["Casing_in_D"] = 0.1158

        well_designer_object_casing(branch_num=0, objects_table=[
            {"name": "Casing_" + str(indx), "top_depth": 0, "bottom_depth": bot_depth, "diameter_in": line["Casing_in_D"],
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

print("Чтение основных данных для скважины {}.".format(well_name))

equip_row_value = excel_row_reader(well_name_in_excel, "Well", equipment_data_list, 5)
wlist_row_value = excel_row_reader(well_name_in_excel, "Well", well_names_list, 5)
summary_row_value = excel_row_reader(well_name_in_excel, "Well", summary_data_list, 5)

####### Задаем basic data ####################################################
set_well_basic_data(well_name, summary_row_value)

####### Читаем конструкцию ###################################################
# Берем данные из колонок с 19 по 27 с листа 'equipment_data_list'
label_value = equip_row_value["Label.1"].values[0][:-1].split("|")
type_value = equip_row_value["Type.1"].values[0][:-1].split("|")
# label_value = data_reader("Label.1", "", equip_row_value, well_name_in_excel)
# type_value = data_reader("Type.1", "", equip_row_value, well_name_in_excel)

md_value = data_reader("Measured Depth, feet", "feet", equip_row_value, well_name_in_excel)
tub_in_d_value = data_reader("Tubing Inside Diameter, inches", "inches", equip_row_value, well_name_in_excel)
tub_out_d_value = data_reader("Tubing Outside Diameter, inches", "inches", equip_row_value, well_name_in_excel)
casing_in_d_value = data_reader("Casing Inside Diameter, inches", "inches", equip_row_value, well_name_in_excel)
tub_in_roughness_value = data_reader("Tubing Inside Roughness, inches", "inches", equip_row_value, well_name_in_excel)
tub_out_roughness_value = data_reader("Tubing Outside Roughness, inches", "inches", equip_row_value, well_name_in_excel)
casing_in_roughness_value = data_reader("Casing Inside Roughness, inches", "inches", equip_row_value, well_name_in_excel)

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
