#1 BTU/lb∙°F = 4186.8 J/kg∙K

import pandas as pd
import numpy as np

##################  FOR DEBUG  #########################################

# Чтение данных с указанного листа из excel
def excel_row_reader(well_name: str, list_name: str, srip_rows: int):
    # Чтение из excel листов / убираем пустые строки
    try:
        data_from_list = pd.read_excel(fileIn, sheet_name=list_name, header=0, skiprows=srip_rows)
        data_from_list.dropna(subset=["Well"], inplace=True)

        row_value = data_from_list.loc[data_from_list["Well"] == well_name]
    except:
        raise SystemExit("Unable to get data from excel file!")

    # Проверяем на ошибки
    if len(row_value) == 0:
        raise SystemError("There is no data for well with name '{}' in excel file!".format(well_name))

    return row_value

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
        if units == "number":
            df_out = np.array(df_out, dtype="float") * 1
        if units == "":
            #df_out = np.array(df_out, dtype="float") * 1
            df_out = df_out
    except Exception:
        print("Error with well {}".format(well_name))

    return df_out


##################  FOR DEBUG  #########################################

fileIn = "D:\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
#fileIn = "D:\Work\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"

well_names_list = "WellList"
equipment_data_list = "EquipmentData"
summary_data_list = "SummaryData"
vlp_data_list ="VLPIPRData"
ipr_data_list ="IPRData"

ipr_phase = "liquid"
well_type = "producer"

current_well_name = "W_SHR_220_BB"

##################  FOR DEBUG  #########################################


#current_well_name = get_project_name ()

equip_row_value = excel_row_reader(current_well_name, equipment_data_list, 5)

# Читаем Average Heat Capacities
# Берем данные из колонок с 29 по 35 с листа 'equipment_data_list'
cp_oil = data_reader("Cp Oil, BTU/lb/F", "btu", equip_row_value, current_well_name)
cp_gas = data_reader("Cp Gas, BTU/lb/F", "btu", equip_row_value, current_well_name)
cp_water = data_reader("Cp Water, BTU/lb/F", "btu", equip_row_value, current_well_name)

# Читаем Average Heat Capacities
# Берем данные из колонок с 33 по 35 с листа 'equipment_data_list'
wd_heat_transfer_use_parameters (enabled=True)

wd_heat_transfer_adjust_specific_heat_capacity (enabled=True,
      specific_heat_gas=cp_gas,
      specific_heat_water=cp_water,
      specific_heat_oil=cp_oil)

#md_value = data_reader("Formation MD, feet", "feet", equip_row_value)
tvd_value = data_reader("Formation TVD, feet", "feet", equip_row_value, current_well_name)
temp_value = data_reader("Formation Temperature, deg F", "F", equip_row_value, current_well_name)

#TODO: проверить единцы измерения
heat_transfer_value = float(equip_row_value["HTC.1"].values[0])

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