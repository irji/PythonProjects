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


print("Чтение данных по IPR для скважины {}.".format(current_well_name))

#current_well_name = well_name_in_excel
#current_well_name = get_well_name(name, "_", 2)

ipr_row_value = excel_row_reader(current_well_name, "Well", ipr_data_list, 5)

#dates_value = data_reader("Date", "date", ipr_row_value, current_well_name)
ipr_rate_value = data_reader("Rate, STB/day", "STB/day", ipr_row_value, current_well_name)

if ipr_rate_value.size == 1: # Если в ячейке только одно значение, а не массив
    rate_value = np.array([ipr_rate_value])

ipr_pressure_value = data_reader("Pressure, psig.1", "psig", ipr_row_value, current_well_name)
ipr_pressure_value[ipr_pressure_value < 0] = 0.01 # убирает отрицательные значения

if ipr_pressure_value.size == 1:  # Если в ячейке только одно значение, а не массив
    pressure_value = np.array([ipr_pressure_value])

res_temp_value = data_reader("Reservoir Temperature, deg F", "F", ipr_row_value, current_well_name) # Понадобится в 23.3 когда поле для температуры появится
res_pressure_value = data_reader("Reservoir Pressure, psig", "psig", ipr_row_value, current_well_name)

pi_entry_value = data_reader("Productivity Index, STB/day/psi", "STB/day/psi", ipr_row_value, current_well_name)

res_model = int(data_reader("Reservoir Model", "number", ipr_row_value, current_well_name))


if ipr_rate_value.size != 0 and ipr_pressure_value.size != 0:

    # Формируем массив с данными по измерениям
    sample_data = {"volume_rate" : ipr_rate_value, "bhp" : ipr_pressure_value, "reservoir_pressure" : 0}
    df_sample_data = pd.DataFrame(sample_data)
    df_sample_data = df_sample_data.to_dict('records')

    wd_create_ipr_curve(ipr = "IPR_Table", ignore_if_exists=True)
    wd_create_ipr_curve(ipr = "IPR", ignore_if_exists=True)

    wd_adjust_ipr_well_test_data (ipr = "IPR_Table",
          use_date=False,
          date=datetime (year=2023, month=1, day=1, hour=0, minute=0, second=0),
          change_ipr_base=False,
          ipr_base=ipr_phase,
          change_model=True,
          use_well_test_data=True,
          well_test_data_type="multipoint",
          well_test_data=df_sample_data)

    wd_adjust_ipr_parameters(ipr="IPR_Table",
                             use_date=False,
                             date=datetime(year=2023, month=7, day=17, hour=0, minute=0, second=0),
                             ipr_base=ipr_phase,
                             ipr_model="pi_entry",
                             pi_entry_reservoir_pressure=res_pressure_value,
                             pi_entry_productivity_index=pi_entry_value,
                             pi_entry_vogel_coefficient=0.2,
                             pi_entry_use_calculated_bubble_point_pressure=False,
                             pi_entry_bubble_point_pressure=120)

    if res_model > 1:
        print("Значение \"Reservoir Model\" = {} не поддержано.".format(res_model))

else:
    #print("Немогу получить данные по IPR для скважины '{}'!".format(current_well_name))
    print_log(text="Немогу получить данные по IPR для скважины '{}'!".format(current_well_name), severity="warning")