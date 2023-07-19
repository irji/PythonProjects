#1 BTU/lb∙°F = 4186.8 J/kg∙K

current_well_name = get_project_name ()

equip_row_value = excel_row_reader(current_well_name, equipment_data_list, 5)

# Читаем Average Heat Capacities
# Берем данные из колонок с 29 по 35 с листа 'equipment_data_list'

# cp_oil = float(equip_row_value["Cp Oil, BTU/lb/F"].values[0]) * 4.1863 # Перевод единиц
# cp_gas = float(equip_row_value["Cp Gas, BTU/lb/F"].values[0]) * 4.1863 # Перевод единиц
# cp_water = float(equip_row_value["Cp Water, BTU/lb/F"].values[0]) * 4.1863 # Перевод единиц

cp_oil = data_reader("Cp Oil, BTU/lb/F", "btu", equip_row_value)
cp_gas = data_reader("Cp Gas, BTU/lb/F", "btu", equip_row_value)
cp_water = data_reader("Cp Water, BTU/lb/F", "btu", equip_row_value)

# Читаем Average Heat Capacities
# Берем данные из колонок с 33 по 35 с листа 'equipment_data_list'
wd_heat_transfer_use_parameters (enabled=False)

wd_heat_transfer_adjust_specific_heat_capacity (enabled=True,
      specific_heat_gas=cp_gas,
      specific_heat_water=cp_water,
      specific_heat_oil=cp_oil)

#md_value = data_reader("Formation MD, feet", "feet", equip_row_value)
tvd_value = data_reader("Formation TVD, feet", "feet", equip_row_value)
temp_value = data_reader("Formation Temperature, deg F", "F", equip_row_value)

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