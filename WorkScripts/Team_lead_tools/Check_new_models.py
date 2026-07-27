import pathlib
import os

#================================ USER SETTINGS ================================
user_names= [
    "georgii.kostin",
    "konstantin.vorobev",
    "polina.tsvetkova",
    "german.nepotasov",
    "dmitrii.bevzenko",
    "olga.fedyaeva",
    "dmitry.kliymenko",
    "pavel.koryuzlov",
    "andrey.spiridonov",
    "aleksandr.timoshenko",
    "aigul.khatmullina",
    "ahmed.alkebsi"
]
#================================ USER SETTINGS ================================

#================================ FILES SETTINGS ================================
files_ext = ["dat", "data", "afi", "snp", "sdata", "py", "fcs"]
report_file_name = "report.txt"
#================================ FILES SETTINGS ================================


def check_folder():

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


    if os.path.isfile(os.path.join(__location__, report_file_name)): #удаляем старый файл отчета
        os.remove(os.path.join(__location__, report_file_name))

    for user in user_names:
        #input_path = pathlib.Path("N:\\{}\\NEW_MODELS".format(user))
        input_paths = [pathlib.Path("N:\\{}\\UPDATE_MODELS".format(user)), pathlib.Path("N:\\{}\\NEW_MODELS".format(user))]
        #files_count = 0

        for input_path in input_paths:
            #print("Проверяю папку {}.".format(input_path))
            with open(report_file_name, "a+", encoding="utf-8") as file:
                print("Проверяю папку пользователя {}.".format(user))
                files_count = 0
                file.write("Проверяю папку пользователя {}.\n".format(user))

                for f_ext in files_ext:
                    for item in input_path.rglob("*." + f_ext):
                        is_md_project = False
                        if item.is_file():
                            
                            if str(item).__contains__(" ") and f_ext != "sdata" and f_ext != "py":
                                print("Путь и название файла не должен содержать пробелы! {}".format(item))
                                file.write("Путь и название файла не должен содержать пробелы! {}\n".format(item))

                            if str(item).__contains__(".snf") and f_ext != "sdata" and f_ext != "py":
                                print("Рекомендуется почистить проект ДМ/ДГ от ранее выгруженных моделей. {}".format(item))
                                file.write("Рекомендуется почистить проект ДМ/ДГ от ранее выгруженных моделей.  {}\n".format(item))
                                is_md_project = True

                            if len(item.parts) != 8: #проверяем что путь до файла модели состоит строго из 8 частей
                                # пример того что приходит в item.parts ('N:\\', 'ahmed.alkebsi', 'NEW_MODELS', 'models.E100', '2026-1-tNav', 'JOB_Tomori', '#134938', 'HM_FINAL_21_SEPT24_1_FixedPVT_DPCDT_OneEquil_HM_FC.data')
                                if len(item.parts) < 8: #если путь состоит менее чем из 8 частей, то скорее всего прощен уровень вложенности
                                    print("Пропущено одна или несколько вложенных папок. Нужно исправить путь размещения модели. {}".format(item))
                                    file.write("Пропущено одна или несколько вложенных папок. Нужно исправить путь размещения модели. {}\n".format(item))
                                else:
                                    #если путь состоит из более 8 частей, то есть "лишние" папки содержащие файлы из списка files_ext
                                    #if not item.parts.__contains__("DATA.ORI"): #игнорируем папку DATA.ORI
                                    if not str(item).__contains__("DATA.ORI"):  # игнорируем папку DATA.ORI
                                        if str(item).__contains__("RESULTS") and is_md_project == False:
                                            print("Возможно папку RUSULTS нужно удалить. Она нужна для рестарта? {}".format(item))
                                            file.write("Возможно папку RUSULTS нужно удалить. Она нужна для рестарта? {}\n".format(item))

                            if not item.parts[4].__contains__("tNav") and f_ext == "data": # проверям что папка с номером не содержит tNav в названии и файл с расширением data
                                if item.parts[-1].split(".")[1].islower() and is_md_project == False:
                                    print("Расширение должно быть указано заглавными буквами. {}".format(item))
                                    file.write("Расширение должно быть указано заглавными буквами. {}\n".format(item))

                            if item.parts[-1].__contains__("py"): # проверям что в модели нет python скриптов
                                if not item.parts.__contains__("USER"):
                                    print("Необходимо проверить пишет ли что-нибудь python скрипт на диск и в какую папку. {}".format(item))
                                    file.write("Необходимо проверить пишет ли что-нибулдь python скрипт на диск и в какую папку. {}\n".format(item))

                            if not str(item).__contains__("nexus") and not str(item).__contains__("NEXUS"):
                                if f_ext == "dat" or f_ext == "data" or f_ext == "snp" or f_ext == "afi" or f_ext == "fcs":
                                    files_count+=1
                                    print(item)

                print("Папка пользователя {}/{} содержит \"{}\" файлов \"data\\dat\\snp\\afi\".".format(input_path.name, user, files_count))
                file.write("Папка пользователя {} содержит \"{}\" файлов \"data\\dat\\snp\\afi\".\n".format(user, files_count))

        print(" ")

if __name__ == '__main__':
    check_folder()