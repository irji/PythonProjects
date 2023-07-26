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


print("Чтение данных по IPR для скважины {}.".format(current_well_name))

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

    wd_create_ipr_curve(ipr= current_well_name + "_IPR", ignore_if_exists=True)

    wd_adjust_ipr_well_test_data (ipr=current_well_name + "_IPR",
          use_date=False,
          date=datetime (year=2023, month=1, day=1, hour=0, minute=0, second=0),
          change_ipr_base=False,
          ipr_base=ipr_phase,
          change_model=True,
          use_well_test_data=True,
          well_test_data_type="multipoint",
          well_test_data=df_sample_data)

    # Если вдруг для Well PI понадобиться матчинг
    # if res_model == 0:
    #     wd_ipr_matching(ipr=current_well_name + "_IPR",
    #                     ipr_base=ipr_phase,
    #                     result_name=current_well_name + "_IPR_Matched",
    #                     overwrite_result=False,
    #                     algorithm="Particle Swarm Optimization",
    #                     max_iterations=10000,
    #                     stop_on_slow_improvement=True,
    #                     improvement_iterations=1000,
    #                     improvement_value=2,
    #                     correlation_types=[{"corr_type": "well_pi"}],
    #                     correlation_table=[{"variable": "wellpi_reservoir_pressure_liquid", "use_for_matching": True,
    #                                         "min": 0.000001, "base_value": 250, "max": 500},
    #                                        {"variable": "wellpi_productivity_index_liquid", "use_for_matching": False,
    #                                         "min": 0.000001, "base_value": 50, "max": 100}])

    if res_model == 0:
        wd_adjust_ipr_parameters(ipr=current_well_name + "_IPR",
             use_date=False,
             date=datetime (year=2023, month=1, day=1, hour=0, minute=0, second=0),
             ipr_base=ipr_phase,
             ipr_model="well_pi",
             wellpi_reservoir_pressure=res_pressure_value,
             wellpi_productivity_index=pi_entry_value)

    if res_model == 1:
        wd_ipr_matching(ipr=current_well_name + "_IPR",
            ipr_base=ipr_phase,
            result_name=current_well_name + "_IPR_Matched",
            overwrite_result=False,
            algorithm="Particle Swarm Optimization",
            max_iterations=10000,
            stop_on_slow_improvement=True,
            improvement_iterations=1000,
            improvement_value=2,
            correlation_types=[{"corr_type": "vogel"}],
            correlation_table=[
                {"variable": "vogel_reservoir_pressure", "use_for_matching": False, "min": 0.000001,
                 "base_value": res_pressure_value, "max": res_pressure_value * 3},
                {"variable": "vogel_coefficient", "use_for_matching": True, "min": 0, "base_value": 0.5,
                 "max": 1},
                {"variable": "vogel_max_rate", "use_for_matching": True, "min": 0, "base_value": 2500,
                 "max": 5000}])

    if res_model > 1:
        print("Значение \"Reservoir Model\" = {} не поддержано.".format(res_model))

else:
    #print("Немогу получить данные по IPR для скважины '{}'!".format(current_well_name))
    print_log(text="Немогу получить данные по IPR для скважины '{}'!".format(current_well_name), severity="warning")