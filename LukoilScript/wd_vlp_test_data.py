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
        raise SystemExit("Ошибка чтения данных из excel файла!")

    # Проверяем на ошибки
    if len(row_value) == 0:
        raise SystemError("Нет данных для скважины '{}' в excel файле!".format(well_name))

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
        print("Ошибка чтения данных для скважины {}".format(well_name))

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




vlp_row_value = excel_row_reader(current_well_name, vlp_data_list, 5)
summary_row_value = excel_row_reader(current_well_name, summary_data_list, 5)

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

# Формируем массив с данными по измерениям
sample_data = {"thp" : thp_value, "flo" : rate_value, "wfr" : wct_value, "gfr" : gor_value, "alq" : pump_value,
               "gauge" : gauge_depth__value, "bhp" : gauge_press_value, "temperature" : temp_value, "comment" : comment_value}
df_sample_data = pd.DataFrame(sample_data)
df_sample_data = df_sample_data.to_dict('records')

well_project_adjust_well_test_data (well_type=well_type,
      sample_name="Test1",
      table=df_sample_data,
      flo_type="LIQ", wfr_type="WCT", gfr_type="GOR", alq_type="PUMP", tqb_type="BHP")