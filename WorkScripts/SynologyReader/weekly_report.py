from synology_drive_api.drive import SynologyDrive
from openpyxl import load_workbook
import pandas as pd


def aggregate_comments(input_dataframe):
    test = input_dataframe.groupby(['Тема'])

    for gr in test:
        print(gr)

    return test




user_name = "georgii.kostin"
employee_name = "Костин Георгий"
user_password = "5MGc/8cac"
server_path = "synoffice.local.rfdyn.ru"
filtered_tabl = None
vertical_concat = None

with SynologyDrive(user_name, user_password, server_path, dsm_version="7") as synology_drive:

    folders = synology_drive.list_folder("/team-folders/Reports/SUPPORT")["data"]["items"]

    for item in folders:
        if item["name"] != "Archive" and item["name"] != "Week Шаблон":
            #print(item["name"])
            path = "/team-folders/Reports/SUPPORT/" + item["name"] + "/2. Report Support Вторник.osheet"

            bio = synology_drive.download_synology_office_file(path)
            tabl = pd.read_excel(bio, sheet_name=None, na_values="nan")["Support"]

            # Фильтруем dataframe только для себя + удаляем строки с пустым значением в колонке 'Тема'
            filtered_tabl = tabl[tabl["Сотрудник"] == employee_name].dropna(subset=["Тема"])
            #filtered_tabl = tabl["Support"]
            vertical_concat = pd.concat([vertical_concat, filtered_tabl], axis=0)


vertical_concat.sort_values(by="Тема", inplace=True)

no_duplicates = vertical_concat.drop_duplicates(subset="Тема")

#test = vertical_concat.groupby("Тема")["Комментарии"].apply(' '.join)

#test = vertical_concat

#test=vertical_concat.groupby(vertical_concat['Тема']).aggregate({"Комментарии": ' '.join })

#test = vertical_concat.groupby(['Тема'])['Комментарии'].aggregate(lambda x : ' '.join(str(x)))

test = aggregate_comments(vertical_concat)

print(vertical_concat)




#if __name__ == '__main__':
#    download_reports()
