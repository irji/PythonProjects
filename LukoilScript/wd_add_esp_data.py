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

def get_well_name(input_well_name_string: str, split_by: str, position: int ):
    well_name = input_well_name_string

    if split_by != "" and position != 0:
        well_name_elements = well_name.split(split_by)
        well_name = well_name_elements[position]

    return well_name

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

current_well_name = "W_SHR_64_BB"

##################  FOR DEBUG  #########################################

#current_well_name = well_name_in_excel

print("Чтение данных по ESP для скважины {}.".format(current_well_name))

try:
    esp_parameters_values = excel_row_reader(current_well_name, "Index Pump", esp_data_list, 5)
    well_esp_name = ""
    first_well_esp_name = ""
    sum_well_esp_name = ""

    taper_stages_values = data_reader("Taper\nStages", "", esp_parameters_values.iloc[[0]], current_well_name)
    esp_HeadY_value_sum = np.zeros(40) # размер равен 1000 деленное на 25, так же как для esp_HeadX_value
    esp_HeadX_value_sum = np.zeros(40)
    eps_base_freq_value_sum = data_reader("Pump Frequency, Herz", "number", esp_parameters_values.iloc[[0]], current_well_name)

    for index in range(0, len(esp_parameters_values)):

        row_value = esp_parameters_values.iloc[[index]]

        esp_name = data_reader("Pump Name", "", row_value, current_well_name)
        eps_manufacturer = data_reader("Pump Manufacturer", "", row_value, current_well_name)
        esp_pump_index = data_reader("Index Pump", "", row_value, current_well_name)
        #esp_freq_index = data_reader("Pump Frequency, Herz", "number", row_value, current_well_name)
        esp_head_coeff = data_reader("Pump Head.Coeff", "number", row_value, current_well_name)
        esp_pow_coeff = data_reader("Pump HP.Coeff", "number", row_value, current_well_name)
        esp_HeadX_value = np.arange(1, 1000, 25, dtype='float')  # Дебит для расчета напора по зависимости
        esp_HeadX_value[1:] = esp_HeadX_value[1:] - 1
        esp_HeadX_value_sum = esp_HeadX_value

        esp_EffY_value = esp_pow_coeff
        esp_PowY_value = esp_pow_coeff
        #eps_HeadX_value = data_reader("Head.X, RB/day", "number", row_value, current_well_name)
        well_esp_name = "{}_{}_{}".format(int(float(esp_pump_index)), eps_manufacturer, esp_name)

        eps_base_freq_value = data_reader("Pump Frequency, Herz", "number", row_value, current_well_name)
        eps_stage_value = data_reader("Pump Stages", "number", row_value, current_well_name)

        # множитель для расчета суммарной характеристики
        mult = float(taper_stages_values[index]) / float(eps_stage_value)

        if len(esp_head_coeff) != 0:
            esp_HeadY_value = (pow(esp_HeadX_value, 5) * esp_head_coeff[0] + pow(esp_HeadX_value, 4) * esp_head_coeff[1] + \
                              pow(esp_HeadX_value, 3) * esp_head_coeff[2] + pow(esp_HeadX_value, 2) * esp_head_coeff[3] + \
                              esp_HeadX_value * esp_head_coeff[4] + esp_head_coeff[5]) * 0.3048 # Конвертируем feet в метры

            esp_PowY_value = (pow(esp_HeadX_value, 5) * esp_pow_coeff[0] + pow(esp_HeadX_value, 4) * esp_pow_coeff[1] + \
                              pow(esp_HeadX_value, 3) * esp_pow_coeff[2] + pow(esp_HeadX_value, 2) * esp_pow_coeff[3] + \
                              esp_HeadX_value * esp_pow_coeff[4] + esp_pow_coeff[5]) * 0.7354985  # Конвертируем ЛС в кВт

            esp_HeadX_value = esp_HeadX_value * 0.15898729  # Конвертируем RB/day в m3/day.

            esp_EffY_value = (0.00011343 * esp_HeadX_value * esp_HeadY_value) / esp_PowY_value

            # расчет суммарной характеристики
            esp_HeadY_value_sum = esp_HeadY_value_sum + esp_HeadY_value * mult

            # Убираем все значения из массивов после того как значения перестали уменьшаться
            # Формируем массив с данными по измерениям
            df_sample_data = esp_cut_relation(esp_HeadX_value, esp_HeadY_value, esp_EffY_value, esp_PowY_value)

            if first_well_esp_name == "":
                first_well_esp_name = well_esp_name
                sum_well_esp_name = "SUM_" + well_esp_name

            # Добавляем насос в библиотеку
            well_designer_esp_catalog_add_esp (name=well_esp_name,
                  base_frequency=eps_base_freq_value,
                  base_stage_number=eps_stage_value,
                  objects_table=df_sample_data)
        else:
            # print("Для скважины {} не найдены коэффициенты для расчета РНХ для насоса.".format(current_well_name))
            print_log(text="Для скважины {} не найдены коэффициенты для расчета РНХ для насоса {}.".format(current_well_name, well_esp_name),
                       severity="warning")

    esp_HeadX_value_sum = esp_HeadX_value_sum * 0.15898729  # Конвертируем RB/day в m3/day.

    # Формируем массив с данными по измерениям с суммарной характеристикой
    df_sample_data_sum = esp_cut_relation(esp_HeadX_value_sum, esp_HeadY_value_sum, esp_EffY_value, esp_PowY_value)

    # Добавляем насос с суммарной характеристикой в библиотеку
    well_designer_esp_catalog_add_esp(name=sum_well_esp_name,
                                      base_frequency=eps_base_freq_value_sum,
                                      base_stage_number=1,
                                      objects_table=df_sample_data_sum)

    esp_row_value = excel_row_reader(current_well_name, "Well", esp_data_list, 5)

    eps_depth_value = data_reader("Pump Depth (Measured), feet", "feet", esp_row_value, current_well_name)
    eps_oper_freq_value = data_reader("Operating Frequency, Herz", "number", esp_row_value, current_well_name)
    eps_stage_value = data_reader("Pump Stages", "number", esp_row_value, current_well_name)
    esp_pump_wear_factor = 1.0 - data_reader("Pump Wear Factor, fraction", "number", esp_row_value, current_well_name)

    well_designer_object_esp (branch_num=0,
          objects_table=[{"name" : "ESP_1", "depth" : eps_depth_value, "status" : "active", "max_gas_vol_fraction" : 1,
                          "operating_frequency" : eps_oper_freq_value, "slippage_factor" : 1, "esp_stage_num" : 1,
                          "head_derating_factor" : esp_pump_wear_factor, "rate_derating_factor" : 1, "esp_catalog" : sum_well_esp_name}])
except Exception as e:
    print_log(text="Для скважины {} нет данных для насоса или данные содержат ошибку!".format(current_well_name),
              severity="warning")
    print(e)
