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

# Убираем все значения из массивов после того как значения перестали уменьшаться
def esp_cut_relation(x_axis: pd.DataFrame, y_axis: pd.DataFrame):
    min_val = np.min(y_axis)

    if min_val < 0:
        for index, elem in np.ndenumerate(y_axis):
            if elem < 0:
                x_axis = x_axis[:index[0]]
                y_axis = y_axis[:index[0]]
                break
    else:
        fliped_HeadY_value = np.flip(y_axis)

        ref_value = fliped_HeadY_value[0]

        for index, elem in np.ndenumerate(fliped_HeadY_value):
            if elem > ref_value:
                y_axis = np.flip(fliped_HeadY_value[index[0] - 1:])
                x_axis = x_axis[:len(y_axis)]
                break
            else:
                ref_value = elem

    # Формируем массив с данными по измерениям
    sample_data = {"rate": x_axis, "head": y_axis, "efficiency": 1, "power": 1}
    df_sample_data = pd.DataFrame(sample_data)
    df_sample_data = df_sample_data.to_dict('records')

    return  df_sample_data

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


print("Чтение данных по VLP для скважины {}.".format(current_well_name))

#current_well_name = well_name_in_excel

vlp_row_value = excel_row_reader(current_well_name, "Well", vlp_data_list, 5)
summary_row_value = excel_row_reader(current_well_name, "Well", summary_data_list, 5)

if summary_row_value["Well Type"].values[0] == 2:
      well_type = "injector"

dates_value = data_reader("Test Point Date", "", vlp_row_value, current_well_name)
comment_value = data_reader("Test Point Comment", "", vlp_row_value, current_well_name)

dates_value = np.char.add(dates_value, "; ")
comment_value = np.char.add(dates_value, comment_value)

thp_value = data_reader("Tubing Head Pressure, psig", "psig", vlp_row_value, current_well_name)
temp_value = data_reader("Tubing Head Temperature, deg F", "F", vlp_row_value, current_well_name)
wct_value = data_reader("Water Cut, %", "%", vlp_row_value, current_well_name)
rate_value = data_reader("Liquid Rate, STB/day", "STB/day", vlp_row_value, current_well_name)
gauge_depth__value = data_reader("Gauge Depth (Measured), feet", "feet", vlp_row_value, current_well_name)
gauge_press_value = data_reader("Gauge Pressure, psig", "psig", vlp_row_value, current_well_name)
gor_value = data_reader("GOR, scf/STB", "scf/STB", vlp_row_value, current_well_name)
pump_value = data_reader("Operating Frequency, Herz", "number", vlp_row_value, current_well_name)

if pump_value.size == 0:
    pump_value = 0

# Формируем массив с данными по измерениям
sample_data = {"thp" : thp_value, "flo" : rate_value, "wfr" : wct_value, "gfr" : gor_value, "alq" : pump_value,
               "gauge" : gauge_depth__value, "bhp" : gauge_press_value, "temperature" : temp_value, "comment" : comment_value}
df_sample_data = pd.DataFrame(sample_data)
df_sample_data = df_sample_data.to_dict('records')

well_project_adjust_well_test_data (well_type=well_type,
      sample_name="Test1",
      table=df_sample_data,
      flo_type="LIQ", wfr_type="WCT", gfr_type="GOR", alq_type="PUMP", tqb_type="BHP")
well_project_adjust_well_test_data (well_type=well_type,
      sample_name="Last_point",
      table=[df_sample_data[-1]],
      flo_type="LIQ", wfr_type="WCT", gfr_type="GOR", alq_type="PUMP", tqb_type="BHP")