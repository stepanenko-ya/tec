import psycopg2

conn = psycopg2.connect(
    host='localhost',
    user='stepanenko',
    password='Stomatolog',
    database='test2',
    )
db = conn.cursor()

# tab_num = 't030'
# f_csv = open('/home/stepanenko/Projects/test/test/qwerty.csv', 'r')

# db.execute("copy dbo." + tab_num + " from '/home/stepanenko/Projects/test/test/qwerty.csv' DELIMITER '{' QUOTE E'\b' CSV")

s = '{'
db.execute(f"""select * from dbo.t203 WHERE  refno  LIKE '%{s}%' """)
print(db.fetchall())
conn.commit()
# db.execute(f"update dbo.{tab_num} set column_1 = replace (column_1, '🔶', '@')")



# def update():
# #
# #     # for obliqua in obliqua_lst:
# #         # tab = version.tables.get(obliqua[:3])
#     slash = '{'
#     db.execute(f"update dbo.t203 set RefNo = replace (RefNo, '🔶', '{slash}')")
#     conn.commit()
#
# update()