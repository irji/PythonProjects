import pyodbc

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

res1 = get_wells()

for r in res1:
    #print(r)
    print(get_trajectory_arrays(str(r)))