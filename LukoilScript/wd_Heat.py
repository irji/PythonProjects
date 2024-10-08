#1 BTU/lb∙°F = 4186.8 J/kg∙K

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

well_name_in_excel = "W_SHR_64_BB"
#well_name_in_excel = "W_SHR_220_BB"
well_name = "64_BB"

##################  FOR DEBUG  #########################################

print("Чтение данных по Heat Capacities для скважины {}.".format(well_name))

equip_row_value = excel_row_reader(well_name_in_excel, "Well", equipment_data_list, 5)

# Читаем Average Heat Capacities
# Берем данные из колонок с 29 по 35 с листа 'equipment_data_list'
cp_oil = data_reader("Cp Oil, BTU/lb/F", "btu", equip_row_value, well_name_in_excel)
cp_gas = data_reader("Cp Gas, BTU/lb/F", "btu", equip_row_value, well_name_in_excel)
cp_water = data_reader("Cp Water, BTU/lb/F", "btu", equip_row_value, well_name_in_excel)

# Читаем Average Heat Capacities
# Берем данные из колонок с 33 по 35 с листа 'equipment_data_list'
wd_heat_transfer_use_parameters (enabled=True)

wd_heat_transfer_adjust_specific_heat_capacity (enabled=True,
      specific_heat_gas=cp_gas,
      specific_heat_water=cp_water,
      specific_heat_oil=cp_oil)

#md_value = data_reader("Formation MD, feet", "feet", equip_row_value)
tvd_value = data_reader("Formation TVD, feet", "feet", equip_row_value, well_name_in_excel)
temp_value = data_reader("Formation Temperature, deg F", "F", equip_row_value, well_name_in_excel)

#TODO: проверить единцы измерения. Пока предполагаю, что btu/h/ft2/F (5.67826334)
heat_transfer_value = data_reader("HTC.1", "btu/h/ft2/F", equip_row_value, well_name_in_excel)

# Формируем массивы с данными по траектории и форматируем в виде пригодным для передачи в функцию в
tempvd_data = {"depth": tvd_value, "temperature": temp_value}
df_tempvd = pd.DataFrame(tempvd_data)
df_tempvd = df_tempvd.to_dict('records')

wd_heat_transfer_adjust_tubing_heat_transfer (heat_transfer_type="constant",
      const_heat_transfer=heat_transfer_value,
      clear_table=True,
      table=[])

wd_heat_transfer_adjust_depth (depth_type="tvd")

wd_heat_transfer_adjust_temperature_along_the_wellbore (temperature_type="table",
      const_temp=15.56,
      clear_table=True,
      table=df_tempvd)