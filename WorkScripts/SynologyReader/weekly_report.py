import openpyxl.styles.borders
from synology_drive_api.drive import SynologyDrive
from openpyxl import load_workbook
import pandas as pd
import datetime
import shutil
from copy import copy

import getpass
import keyring

from RandomTest import new_month

exclude_headers = {"Заполнение отчета",
                   "Переписка в почте, сообщения в редмайне, рокетчате, звонки в зуме. Обсуждения с коллегами рабочих вопросов.",
                   "Ежедневное собрание группы",
                   "Ежедневное собрание группы + подгруппы",
                   "Интерфейс",
                   "Еженедельная лекция",
                   "Корпоратив"}

user_name = "georgii.kostin"
employee_name = "Костин Георгий"
user_password = "5MGc/8cac"
server_path = "synoffice.local.rfdyn.ru"
template_name = "Kostin_Georgii_template.xlsx"

def get_monday (date):
  return date  - datetime.timedelta(days=date.weekday() % 7)

def get_friday (date):
  return get_monday (date) + datetime.timedelta (days = 4)


def aggregate_comments(input_dataframe):
    input_dataframe = input_dataframe.reset_index(drop=True).fillna("")

    # делаем группировку по колонке с темой, чтобы одинаковые задачи собрать
    grouped_dataframe = input_dataframe.groupby(['Тема'])
    result_dataframe = None

    for header, df in grouped_dataframe:
        new_comment = ""
        new_id = None
        new_header = str(header[0]).rstrip()

        # проверм что темы нет в списке исключений и объединяем все комментарии
        if new_header not in exclude_headers:
            for row in df.iterrows():
                comment = str(row[1]["Комментарии"])
                new_id = row[1]["#"]
                #new_header = row[1]["Тема"]

                if comment not in new_comment:
                    new_comment = new_comment + comment + "; "

            new_comment = new_comment.rstrip().removesuffix(";")
            data = {"#":[new_id], "Тема":[new_header], "Комментарии":[new_comment]}

            result_dataframe = pd.concat([result_dataframe, pd.DataFrame(data)], axis=0)

    return result_dataframe

def create_path_list(folder_name1, folder_name2):
    paths = []

    paths.append("/team-folders/Reports/SUPPORT/" + folder_name1 + "/3. Report Support Среда.osheet")
    paths.append("/team-folders/Reports/SUPPORT/" + folder_name1 + "/4. Report Support Четверг.osheet")
    paths.append("/team-folders/Reports/SUPPORT/" + folder_name1 + "/5. Report Support Пятница.osheet")

    paths.append("/team-folders/Reports/SUPPORT/" + folder_name2 + "/1. Report Support Понедельник.osheet")
    paths.append("/team-folders/Reports/SUPPORT/" + folder_name2 + "/2. Report Support Вторник.osheet")

    return  paths

def get_task_list_for_report():
    vertical_concat = None

    with SynologyDrive(user_name, user_password, server_path, dsm_version="7") as synology_drive:
        folders = synology_drive.list_folder("/team-folders/Reports/SUPPORT")["data"]["items"]

        path_list = create_path_list(folders[1]["name"], folders[2]["name"])

        for path in path_list:
            #if item["name"] != "Archive" and item["name"] != "Week Шаблон":
                #print(item["name"])
                #path = "/team-folders/Reports/SUPPORT/" + item["name"] + "/3. Report Support Среда.osheet"

                report_file = synology_drive.download_synology_office_file(path)
                tabl = pd.read_excel(report_file, sheet_name=None, na_values="nan")["Support"]

                # Фильтруем dataframe только для себя + удаляем строки с пустым значением в колонке 'Тема'
                filtered_tabl = tabl[tabl["Сотрудник"] == employee_name].dropna(subset=["Тема"])
                vertical_concat = pd.concat([vertical_concat, filtered_tabl], axis=0)

    vertical_concat.sort_values(by="Тема", inplace=True)
    task_list = aggregate_comments(vertical_concat)
    idx = pd.Index(range(0, len(task_list.index), 1))
    task_list = task_list.set_index(idx)

    return task_list

def fill_xls_report(task_list):
    date_string = ""
    new_month_id = "0" + str(datetime.datetime.today().month) if datetime.datetime.today().month < 10 else str(datetime.datetime.today().month)
    new_day_id = "0" + str(datetime.datetime.today().day) if datetime.datetime.today().day < 10 else str(datetime.datetime.today().day)

    date_string = str(datetime.datetime.today().year) + new_month_id + new_day_id
    new_file_name = template_name.replace("template", date_string)
    #shutil.copy(template_name, new_file_name)

    wb = load_workbook(filename = template_name)
    sheet_ranges = wb['Tasks']

    for i,task in task_list.iterrows():
        sheet_ranges.cell(row=i + 3, column=1).value = task["#"]
        sheet_ranges.cell(row=i + 3, column=4).value = task["Тема"]
        sheet_ranges.cell(row=i + 3, column=5).value = task["Комментарии"]

    wb.save(new_file_name)

    #print(task_list)

#print(task_list)

if __name__ == '__main__':
    task_list = get_task_list_for_report()

    fill_xls_report(task_list)