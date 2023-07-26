# Создание WD проектов на основе excel файла
import pandas as pd
import numpy as np

# Путь до excel фала, названия листов с которых данные читаем
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

# Чтение из excel листов / убираем пустые строки
df_well_basic_data = pd.read_excel(fileIn, sheet_name=well_names_list, header=0, skiprows=5)
df_well_basic_data.dropna(subset=["Well"], inplace=True)

df_equipment_data = pd.read_excel(fileIn, sheet_name=equipment_data_list, header=0, skiprows=5)
df_equipment_data.dropna(subset=["Well"], inplace=True)

############################################
#row_value = equipment_data.loc[equipment_data["Well"] == "W_SHR_221_BB"]
############################################

# # Вычисление траектории по MD, TVD
# #well_md = np.array(row_value["MD, feet"].values[0].split("|"), dtype="float")
# well_md = row_value["MD, feet"].values[0].split("|")
# well_md = list(filter(None, well_md))
# well_md = np.array(well_md, dtype="float") * 0.3048
# well_dmd = np.diff(well_md, prepend=0)
#
# well_tvd = row_value["TVD, feet"].values[0].split("|")
# well_tvd = list(filter(None, well_tvd))
# well_tvd = np.array(well_tvd, dtype="float") * 0.3048
# well_dtvd = np.diff(well_tvd, prepend=0)
#
# new_x_coord = np.sqrt(well_dmd*well_dmd - well_dtvd*well_dtvd)
#
# track_data = { "X": np.cumsum(new_x_coord), "Y": 0*np.arange(len(well_md)), "MD": well_md, "TVD": well_tvd }
#
# well_track = pd.DataFrame(track_data)

#print(well_track)

# Создаем словарь "имя скважины" - "имя скважины в excel файле"
well_names = df_well_basic_data["Well"].str.split("_", expand=True)
well_names = well_names[well_names.columns[2]]
new_dict = dict(zip(well_names, df_well_basic_data["Well"]))

for well_name in df_well_basic_data["Well"]:

    row_value = df_equipment_data.loc[df_equipment_data["Well"] == well_name]
    well_1x = 0
    well_1y = 0
    #well_1tvd = 0

# # Если траекторий нет, то созадем новые траектории по по MD, TVD
#     well_md = row_value["MD, feet"].values[0][:-1].split("|")
#     well_md = np.array(well_md, dtype="float") * 0.3048  # Конвертируем feet в метры
#
#     well_tvd = row_value["TVD, feet"].values[0][:-1].split("|")
#     well_tvd = np.array(well_tvd, dtype="float") * 0.3048  # Конвертируем feet в метры
#
#     # Формируем массивы с данными по траектории и форматируем в виде пригодным для передачи в функцию в
#     track_data = {"md": well_md, "x": 0, "y": 0, "z": well_tvd}
#     df_well_track = pd.DataFrame(track_data)
#     df_well_track = df_well_track.to_dict('records')
#
#     well_1tvd = well_tvd[0]
#
#     wells_create(well_name=well_name,
#                  remove_existing_main_branch=False,
#                  branch_num=0,
#                  trajectory_table=df_well_track,
#                  date=datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0),
#                  table=None,
#                  perforations_table=[])

# Если скважины уже есть в проекте, то берем данные с траекторий
    try:
        name_param = str(well_name).split("_")

        excel_well_name = new_dict.get(name_param[2])

        existing_well = get_well_by_name(name=name_param[2])
        existing_well_track = existing_well.get_trajectory_points()
        well_1x = existing_well_track[0][1]
        well_1y = existing_well_track[0][2]
        well_1tvd = existing_well_track[0][3]

        create_well_project_by_well(wells=[{"well": name_param[2]}])
        #project_manager_create_project(projects_table=[{"project_type": "vfp_project", "project_name": well_name}])

        import_workflow(params_table=[
            {"project_type": "vfp_project", "project_name": name_param[2], "file_name": "WF/RFD_workflow.py", "workflow": "RFD_workflow"}],
                        replace_existing=True)

        run_project_workflow(project_type="vfp_project", project_name=name_param[2], workflow="RFD_workflow",
                            variable_types={"EXCEL_FILE_WELL_NAME": "string", "EXCEL_FILE": "string", "TVD_VAR": "real", "VAR_X": "real", "VAR_Y": "real"},
                            variables_object = {"EXCEL_FILE_WELL_NAME": excel_well_name, "EXCEL_FILE": fileIn, "TVD_VAR": well_1tvd, "VAR_X": well_1x, "VAR_Y": well_1y})
    except Exception as e:
        print_log(text="Невозможно создать проект для скважины {}. Возможно такой скважины нет в проекте!".format(well_name),
                  severity="warning")
        print(e)
