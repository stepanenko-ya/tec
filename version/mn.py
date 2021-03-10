
import version
import os
import pymssql
import py7zr
import shutil
import math
from sys import argv
import sys

conn = pymssql.connect(
    server="10.175.1.60:1433",
    user="importer_doc",
    password='QAZxsw123',
    database="Test")
db = conn.cursor()




def create_table(tab_num, arch_file):

    num = version.tables.get(tab_num)

    column_name = ""
    for col in num:
        column_name += col["name"] + " NVARCHAR(" + str(col["length"]) + "), "
        command_create = "CREATE TABLE  t" + tab_num + " (" + column_name[:-2] + ")"

    db.execute("IF (OBJECT_ID('t" + tab_num + "') IS NULL) EXEC('" + command_create + "')")
    conn.commit()

    return tab_num


def file_parsing(unpack_file):

    val = []
    path_to_file = "unpacked_data" + "/" + unpack_file
    tab_num = unpack_file[:3]
    print(tab_num)
    file = open(path_to_file, 'r')
    print("Запись данных в ", unpack_file[:3], " таблицу")
    for row in file:
        row = row.replace("'", "")
        row = row.replace(",", "")
        step = 0
        string_data = ""
        num = version.tables.get(tab_num)
        for column in num:
            data = row[step:step + column["length"]]
            step += column["length"]
            string_data += data + ","
        list_data = string_data[:-1].split(",")
        val.append(tuple(list_data))
    file.close()
    val_ = tuple(val)
    return val_


def run_sql(tab_num, values):
    num = version.tables.get(tab_num)

    col_numbers = "%s, " * len(num)
    replacement = col_numbers[0:-2]
    step = 0
    nxt = 300

    sql = "insert into t" + tab_num + " values(" + replacement + ")"

    cycle = math.ceil(len(values) / nxt)

    try:
        conn = pymssql.connect(server="10.175.1.60:1433", user="importer_doc", password='QAZxsw123', database="Test")
        db = conn.cursor()

        for _ in range(1, cycle + 1):
            db.executemany(sql, values[step:step + nxt])
            conn.commit()
            step += nxt

    finally:
        conn.close()
    return "ok"


def func_truncate():
    dict_tables = version.tables.keys()
    print(dict_tables)
    for tab in dict_tables:
        trunc = "TRUNCATE TABLE t" + tab + ""
        db.execute("IF (OBJECT_ID('t" + tab + "') IS NOT NULL) EXEC('" + trunc + "')")
        conn.commit()
        print(f"Truncate t{tab}")


def main(unpak_files, arch_file):

    for file in unpak_files:
        if file[-3:] != "GIF":
            table = create_table(file[:3], arch_file)
            values = file_parsing(file)
            run_sql(table, values)

    shutil.rmtree("unpacked_data")
    os.remove("archives/" + arch_file)


if __name__ == '__main__':
    vers = sys.argv[1]

    if vers == "Q1":
        from version import ver1 as version
    if vers == "Q2":
        from version import ver2 as version
    if vers == "Q3":
        from version import ver3 as version
    if vers == "Q4":
        from version import ver4 as version

    field = "BrandNo"
    func_truncate()
    archive_direct = os.listdir("archives")
    for arch_file in archive_direct:
        print("Разархивация файлов...", arch_file)
        archive = py7zr.SevenZipFile("archives/" + arch_file, mode='r')
        archive.extract("unpacked_data")
        all_files = os.listdir("unpacked_data")
        main(all_files, arch_file)



