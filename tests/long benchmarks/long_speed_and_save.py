# IMPORTANT! THIS IS A long_ BENCHMARK TEST. THIS TEST ARE USEFUL, WHEN YOU GET AN ERROR AND YOU NEED MORE OUTPUT

from foxy.database import database
from datetime import datetime
import sys
import os
from typing import Union
sys.path.append(__file__.replace(
    "tests"+os.sep+"benchmarks"+os.sep+"long_speed.py", "src"))

# settings
TABLES: int = 50
CELLS: int = 100000
CELLS_VALUE: str = "TEST123"

database.config["DATABASE"]["AUTOLOAD"] = "No"


def check() -> Union[bool, bool]:
    print("–"*25+"starting foxy test"+"–"*25, file=sys.stderr)
    time_start = datetime.now()
    d = database.database("test_object")
    print("DATABASE CREATE TASK FINISHED (after {} since start)".format(
        str(datetime.now()-time_start)), file=sys.stderr)

    for _ in range(TABLES):
        table = d.createTable()
        for i in range(CELLS):
            table.setCell("A"+str(i), CELLS_VALUE)

    print("TABLE CREATE TASK FINISHED (after {} since start)".format(
        str(datetime.now()-time_start)), file=sys.stderr)
    d.save()

    print("DATABASE SAVE TASK FINISHED (after {} since start)".format(
        str(datetime.now()-time_start)), file=sys.stderr)
    final_time_foxy = datetime.now()

    print("–"*25+"starting sqlite3 test"+"–"*25, file=sys.stderr)
    import sqlite3

    time_start = datetime.now()
    database_sqlite = sqlite3.connect(":memory:")
    cursor = database_sqlite.cursor()
    print("DATABASE CREATE TASK FINISHED (after {} since start)".format(
        str(datetime.now()-time_start)), file=sys.stderr)

    for i in range(TABLES):
        cursor.execute("create table A"+str(i)+"(col text)")
        for j in range(CELLS):
            cursor.execute("insert into A"+str(i)+"(col)\nvalues("+str(j)+")")

    print("TABLE CREATE TASK FINISHED (after {} since start)".format(
        str(datetime.now()-time_start)), file=sys.stderr)
    cursor.fetchall()
    print("DATABASE FETCH TASK FINISHED (after {} since start)".format(
        str(datetime.now()-time_start)), file=sys.stderr)
    final_time_sqlite = datetime.now()

    # load check
    print("–"*25+"starting foxy minimal loading test"+"–"*25, file=sys.stderr)
    data2 = database.database("test_object")
    data2.load()

    print("SUCCESSFUL" if data2.tables.keys() ==
          d.tables.keys() else "FAILED", file=sys.stderr)
    return [data2.tables.keys() == d.tables.keys(), final_time_foxy <= final_time_sqlite]


if __name__ == "__main__":
    check()
