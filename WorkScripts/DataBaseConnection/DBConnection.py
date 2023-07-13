import pyodbc
from datetime import datetime

connection_string = 'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;Trusted_connection=yes;DATABASE=D:\DataBase\Test.db'

def get_wells():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    executing_string = 'SELECT WELLNAME FROM WELLS'

    rows = cursor.execute(executing_string).fetchall()
    return [str(row[0]) for row in rows]


def get_trajectory_arrays(well):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    executing_string = 'SELECT WELLNAME, ELEVATION, WELL_HEAD_X, WELL_HEAD_Y, TRACK FROM WELLS WHERE WELLNAME = ?'

    row = cursor.execute(executing_string, well).fetchone()
    well_id, wh_elevation, wh_x, wh_y, well_track = row

    if not row:
        return None

    md = []
    incl = []
    azi = []

    lines = well_track.split("\n")
    for line in lines[3:]:
        #  MD X Y Z TVD DX DY AZIM INCL DLS
        if len(line) > 0:
          tr_values = line.strip().split()
          md.append(tr_values[0])
          incl.append(tr_values[8])
          azi.append(tr_values[7])

    return [[md, incl, azi], [wh_x, wh_y, wh_elevation], "md_incl_azi"]

#connection_string = 'DRIVER={SQLite3 ODBC Driver};SERVER=localhost;Trusted_connection=yes;DATABASE=Z:\georgii.kostin\DataBase\Test.db'
first_date = datetime.strptime("01.01.1900", '%d.%m.%Y')

def get_prod_lines ():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    executing_string = 'SELECT ROWID, WELL_NAME, DATE, OIL_RATE, WATER_RATE FROM WELL_PRODUCTION'

    rows = cursor.execute (executing_string).fetchall()
    prod_lines = {}

    for row in rows:
        prod_lines[row[0]] = {}
        prod_lines[row[0]]["well"] = row[1]
        prod_lines[row[0]]["date"] = (datetime.strptime(row[2], '%d.%m.%Y') - first_date).days
        prod_lines[row[0]]["oil"]= float(row[3])
        prod_lines[row[0]]["water"]= float(row[4])

    wells = []
    dates = []
    values = []
    columns = ["oil", "water"]

    for line in prod_lines.values ():
        wells.append (line["well"])
        dates.append (line["date"])
        values.append ({key:line[key] for key in columns if key in line.keys ()})

    return [wells, dates, values]

res1 = get_prod_lines()

for r in res1:
    #print(r)
    print(get_trajectory_arrays(str(r)))