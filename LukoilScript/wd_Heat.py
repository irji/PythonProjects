#1 BTU/lb∙°F = 4186.8 J/kg∙K

import pandas as pd
import numpy as np

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


# Путь до excel фала, названия листов с которых данные читаем
fileIn = "D:\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
#fileIn = "D:\Work\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
well_names_list = "WellList"
equipment_data_list = "EquipmentData"

current_well_name = "W_SHR_64_BB"
#current_well_name = get_project_name ()

# Чтение из excel листов / убираем пустые строки
try:
    equipment_data = pd.read_excel(fileIn, sheet_name=equipment_data_list, header=0, skiprows=5)
    equipment_data.dropna(subset=["Well"], inplace=True)

    ############################################
    equip_row_value = equipment_data.loc[equipment_data["Well"] == current_well_name]
    ############################################
except:
    raise SystemExit("Unable to get data from excel file!")

# Проверяем на ошибки
if len(equip_row_value) == 0:
    raise SystemExit("There is no data for well with name '{}' in excel file!".format(current_well_name))

# Читаем Average Heat Capacities
# Берем данные из колонок с 33 по 35 с листа 'equipment_data_list'
cp_oil = float(equip_row_value["Cp Oil, BTU/lb/F"].values[0])
cp_gas = float(equip_row_value["Cp Gas, BTU/lb/F"].values[0])
cp_water = float(equip_row_value["Cp Water, BTU/lb/F"].values[0])

wd_heat_transfer_adjust_specific_heat_capacity (enabled=False,
      specific_heat_gas=cp_gas,
      specific_heat_water=cp_water,
      specific_heat_oil=cp_oil)