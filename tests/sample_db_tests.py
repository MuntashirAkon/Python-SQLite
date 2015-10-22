#!/usr/bin/python3

from sqlite import SQLite
from datetime import datetime
# notice: you don't need to import sqlite3 module

__title__ = 'Sample Database Test'
__version__ = '0.2.0'
__author__ = 'Muntashir Al-Islam'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2015 Muntashir Al-Islam'

"""
    Sample Database Test
    Tasted on v0.2.0
    Note: Error handling will not work on v0.1.0

    Date: 22 Oct, 2015
"""

began = datetime.now()
print("Program starts at:", began)
print("Connecting to Database...", end=' ')

sqlite = SQLite(":memory:")

print("...")

if sqlite.connect_error: raise sqlite.connect_errno(sqlite.connect_error)
else: print("Connected to Database.")

print("Creating a table...", end=' ')
stmt = sqlite.prepare("""CREATE TABLE sample (
        ID integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        Name text
        )""")
stmt.execute()
print("...")
if stmt.error: raise stmt.errno(stmt.error)
else: print("Table created.")
stmt.close()

print("Inserting some values...", end=' ')
name = "Ian McKellen"
stmt = sqlite.prepare("INSERT INTO sample (Name) VALUES (?), (?), (?), (?);")
stmt.bind_param('ssss', name, "Viggo Mortensen", "David Tennant", "Will Smith")
stmt.execute()
print("...")
if stmt.affected_rows > 0:
    print(stmt.affected_rows, "rows added.")
    print("Last inserted id:", stmt.insert_id)
stmt.close()

print("Outputting the table...", end=' ')
stmt = sqlite.prepare("SELECT * FROM sample")
stmt.execute()
print("...")
stmt.store_result()
print("Table: sample")
if stmt.num_rows > 0:
    name = []
    id = []
    print("+----+--------------------+")
    print("| ID |        Name        |")
    print("+----+--------------------+")
    for i in range(0, stmt.num_rows):
        stmt.bind_result(id, name)
        stmt.fetch()
        print("| {:2} | {:18} |".format(id[0], name[0]))
    print("+----+--------------------+")
stmt.close()

print("updating a value...", end=' ')
stmt = sqlite.prepare("UPDATE sample SET Name=? WHERE ID=?;")
stmt.bind_param('si', "Aragorn II Elessar", 2)
stmt.execute()
print("...")
if stmt.affected_rows > 0:
    print(stmt.affected_rows, "row(s) modified.")
if stmt.error: raise stmt.errno(stmt.error)
stmt.close()

print("Outputting the table again...", end=' ')
stmt = sqlite.prepare("SELECT * FROM sample")
stmt.execute()
print("...")
stmt.store_result()
print("Table: sample")
if stmt.num_rows > 0:
    name = []
    id = []
    print("+----+--------------------+")
    print("| ID |        Name        |")
    print("+----+--------------------+")
    for i in range(0, stmt.num_rows):
        stmt.bind_result(id, name)
        stmt.fetch()
        print("| {:2} | {:18} |".format(id[0], name[0]))
    print("+----+--------------------+")
stmt.close()

print("Deleting an item...", end='')
stmt = sqlite.prepare("DELETE FROM sample WHERE ID=?")
stmt.bind_param('i', 4)
stmt.execute()
print("...")
if stmt.affected_rows > 0:
    print(stmt.affected_rows, "row(s) deleted.")
if stmt.error: raise stmt.errno(stmt.error)
stmt.close()

print("Outputting the table...", end=' ')
stmt = sqlite.prepare("SELECT * FROM sample")
stmt.execute()
print("...")
stmt.store_result()
print("Table: sample")
if stmt.num_rows > 0:
    name = []
    id = []
    print("+----+--------------------+")
    print("| ID |        Name        |")
    print("+----+--------------------+")
    for i in range(0, stmt.num_rows):
        stmt.bind_result(id, name)
        stmt.fetch()
        print("| {:2} | {:18} |".format(id[0], name[0]))
    print("+----+--------------------+")
stmt.close()
print("Closing the Database connection...")
sqlite.close()
print("Connection closed.")
print("Program ends at:", datetime.now())
print("Execution time:", datetime.now() - began)


"""
Output:
Program starts at: 2015-10-22 15:17:34.523776
Connecting to Database... ...
Connected to Database.
Creating a table... ...
Table created.
Inserting some values... ...
4 rows added.
Last inserted id: 4
Outputting the table... ...
Table: sample
+----+--------------------+
| ID |        Name        |
+----+--------------------+
|  1 | Ian McKellen       |
|  2 | Viggo Mortensen    |
|  3 | David Tennant      |
|  4 | Will Smith         |
+----+--------------------+
updating a value... ...
1 row(s) modified.
Outputting the table again... ...
Table: sample
+----+--------------------+
| ID |        Name        |
+----+--------------------+
|  1 | Ian McKellen       |
|  2 | Aragorn II Elessar |
|  3 | David Tennant      |
|  4 | Will Smith         |
+----+--------------------+
Deleting an item......
1 row(s) deleted.
Outputting the table... ...
Table: sample
+----+--------------------+
| ID |        Name        |
+----+--------------------+
|  1 | Ian McKellen       |
|  2 | Aragorn II Elessar |
|  3 | David Tennant      |
+----+--------------------+
Closing the Database connection...
Connection closed.
Program ends at: 2015-10-22 15:17:34.525550
Execution time: 0:00:00.001799
"""
