# Python SQLite
SQLite Database handler in Python with PHP-MySQLi like syntax

## Documentation
Full documentation is covered in the [wiki page](https://github.com/MuntashirAkon/Python-SQLite/wiki).

Here's an quick example:
``` python
from sqlite import SQLite
# notice: you don't need to import sqlite3 module

sqlite = SQLite(":memory:")

# creates table
stmt = sqlite.prepare("""CREATE TABLE sample (
        ID integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        Name text
        )""")
stmt.execute()
stmt.close()

# insert a value
name = "Muntashir"
stmt = sqlite.prepare("INSERT INTO sample (Name) VALUES (?)")
stmt.bind_param('s', name)
stmt.execute()
if stmt.affected_rows > 0:
    print(stmt.affected_rows, "rows added.")
    print("inserted id:", stmt.insert_id)
stmt.close()

# select from table
stmt = sqlite.prepare("SELECT * FROM sample")
stmt.execute()
stmt.store_result()
if stmt.num_rows > 0:
    name = []
    id = []
    print("ID\tName")
    for i in range(0, stmt.num_rows):
        stmt.bind_result(id, name)
        stmt.fetch()
        print("{}\t{}".format(id[0], name[0]))
stmt.close()
sqlite.close()
```

## Contribute
Contribution is always welcome. If you have better ideas or coding, you can always create a pull request or new issue.

## License
This project is licensed under [MIT License](https://github.com/MuntashirAkon/Python-SQLite/blob/master/LICENSE)
