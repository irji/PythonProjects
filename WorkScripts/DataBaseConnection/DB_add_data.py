import pyodbc
import os

connection_string = 'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;Trusted_connection=yes;DATABASE=D:\DataBase\Test.db'
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

files = os.listdir("LAS")

for fl in files:
    names = fl.replace(".las", "").split("_")

    _lines = open("LAS/" + fl, "r").readlines()
    flag = False
    result_line = ""

    for line in _lines:
        if line.find("~Ascii") == 0:
            flag = True
        if flag is True and line.find("~Ascii") == -1:
            result_line = result_line + line

    executing_string = '''INSERT INTO WELL_LOGS (WELL_NAME, LOG_NAME, LOG_VALUES) VALUES ('{}', '{}', '{}')'''.format(str(names[0]), str(names[1]), result_line)
    cursor.execute(executing_string)
    conn.commit()

