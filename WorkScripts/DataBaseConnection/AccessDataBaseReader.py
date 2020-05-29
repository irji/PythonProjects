# import pyodbc
#
# #connection_string = 'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;Trusted_connection=yes;DATABASE=D:\DataBase\Test.db'
# conn = pyodbc.connect(
#     r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};SERVER=localhost;Trusted_connection=yes;DBQ=C:\\Users\\Georgy\\PycharmProjects\\PythonProjects\\WorkScripts\\DataBaseConnection\\Apache_TNAV.accdb;')
# cursor = conn.cursor()
# cursor.execute('select * from monthly_prod_inj')
#
# for row in cursor.fetchall():
#     print(row)

import datetime

date = datetime.datetime.today().day

print(date)