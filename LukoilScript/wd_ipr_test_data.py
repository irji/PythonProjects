import pandas as pd
import numpy as np

###########################################################

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
def data_reader(name: str, units: str, df: pd.DataFrame):
    df_out = np.array([])

    try:
        df_out = df[name].values[0][:-1].split("|")
    except:
        try:
            if np.isnan(df[name].values[0]) != True:
                df_out = df[name].values[0]
            else:
                df_out = np.array([])
        except:
            df_out = np.array([])

    #if np.isnan(df_out) != True:
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
        df_out = pd.to_datetime(df_out, format="%d/%m/%Y")   # Конвертируем строки в даты.
    if units == "btu":
        df_out = np.array(df_out, dtype="float") * 4.1863  # Конвертируем BTU/lb/F в kJ/kg∙K.
    if units == "":
        df_out = np.array(df_out, dtype="float") * 1
        # except:
        #     df_out = np.array([])

    return df_out


###########################################################

# Путь до excel фала, названия листов с которых данные читаем
fileIn = "D:\Models\Lukoil\WellBackup6 Шершневское мест-ие.xlsm"
#fileIn = EXCEL_FILE

ipr_phase = "liquid" # md_Create_WD_Projects
ipr_data_list ="IPRData"
current_well_name = "W_SHR_220_BB"

###########################################################

ipr_row_value = excel_row_reader(current_well_name, ipr_data_list, 5)

dates_value = data_reader("Date", "date", ipr_row_value)
rate_value = data_reader("Liquid Rate, STB/day", "STB/day", ipr_row_value)
pressure_value = data_reader("Pressure, psig", "psig", ipr_row_value)

ipr_model="vogel"
res_pressure_value = data_reader("Reservoir Pressure, psig", "psig", ipr_row_value)
vogel_coeff_value = data_reader("Correction For Vogel (0-No,1-Yes)", "", ipr_row_value)

# TODO: В эксельке не указаны единицы. Думаю, что это STB/day
correlation_rate_value = data_reader("Test Rate", "STB/day", ipr_row_value)


if dates_value.size != 0 and rate_value.size != 0 and pressure_value.size != 0:
    #print("Unable to get data for IPR for well '{}'!".format(current_well_name))

    # Формируем массив с данными по измерениям
    sample_data = {"volume_rate" : rate_value, "reservoir_pressure" : 0, "bhp" : pressure_value}
    df_sample_data = pd.DataFrame(sample_data)
    df_sample_data = df_sample_data.to_dict('records')

    wd_create_ipr_curve(ipr= current_well_name + "_IPR", ignore_if_exists=True)

    wd_adjust_ipr_parameters(ipr=current_well_name + "_IPR",
                             use_date=False,
                             date=datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0),
                             ipr_base=ipr_phase,
                             ipr_model=ipr_model,
                             vogel_coefficient=vogel_coeff_value,
                             vogel_reservoir_pressure=res_pressure_value,
                             vogel_max_rate=correlation_rate_value,
                             fetkovich_exponent=None,
                             fetkovich_reservoir_pressure=None,
                             fetkovich_max_rate=None,
                             fetkovich_backpressure_constant=None,
                             pi_entry_reservoir_pressure=None,
                             pi_entry_productivity_index=None,
                             pi_entry_vogel_coefficient=None,
                             pi_entry_use_calculated_bubble_point_pressure=False,
                             pi_entry_bubble_point_pressure=None,
                             wellpi_reservoir_pressure=None,
                             wellpi_productivity_index=None,
                             jones_reservoir_pressure=None,
                             jones_a_coefficient=None,
                             jones_b_coefficient=None,
                             darcy_reservoir_pressure=None,
                             darcy_reservoir_temperature=None,
                             darcy_reservoir_permeability=None,
                             darcy_reservoir_thickness=None,
                             darcy_drainage_area=None,
                             darcy_dietz_shape_factor=None,
                             darcy_wellbore_radius=None,
                             darcy_mechanical_skin=None,
                             darcy_vogel_coefficient=None,
                             forchheimer_reservoir_pressure=None,
                             forchheimer_reservoir_temperature=None,
                             forchheimer_reservoir_permeability=None,
                             forchheimer_reservoir_thickness=None,
                             forchheimer_drainage_area=None,
                             forchheimer_dietz_shape_factor=None,
                             forchheimer_wellbore_radius=None,
                             forchheimer_perforation_interval=None,
                             forchheimer_mechanical_skin=None)

    wd_adjust_ipr_well_test_data (ipr=current_well_name + " IPR",
          use_date=False,
          date=datetime (year=2023, month=1, day=1, hour=0, minute=0, second=0),
          change_ipr_base=False,
          ipr_base=ipr_phase,
          change_model=False,
          use_well_test_data=False,
          well_test_data_type="multipoint",
          well_test_data=df_sample_data)