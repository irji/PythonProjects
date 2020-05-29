import pyodbc
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

connection_string = 'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;Trusted_connection=yes;DATABASE=D:\DataBase\Test.db'
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

def get_wells():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    executing_string = 'SELECT WELL_NAME FROM WELLS'

    rows = cursor.execute(executing_string).fetchall()
    return [str(row[0]) for row in rows]


def write_las_to_base():
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


def write_prod_data_to_base(well):
    first_date = '01.01.2018'
    month_count = 28
    water_cut = (random.randint(1, 100)/100)/month_count

    for m1 in range(1,month_count):
        res_date = (datetime.strptime(first_date,'%d.%m.%Y') + relativedelta(months=m1)).strftime('%d.%m.%Y')
        oil_rate = random.randint(50, 150)
        water_rate = round(oil_rate * m1 * water_cut)
        print("{} {} {} {}".format(well, res_date, oil_rate, water_rate))

        executing_string = '''INSERT INTO Well_production (WELL_NAME, DATE, OIL_RATE, WATER_RATE) VALUES ('{}', '{}', 
        '{}', '{}')'''.format(well, res_date, oil_rate, water_rate)
        cursor.execute(executing_string)
        conn.commit()


res1 = get_wells()

for r in res1:
    #print(r)
    #print(get_trajectory_arrays(str(r)))

    write_prod_data_to_base(r)