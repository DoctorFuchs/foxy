from foxy.database import database
from datetime import datetime
import sys
import os
from typing import Union
sys.path.append(__file__.replace(
    "tests"+os.sep+"benchmarks"+os.sep+"save.py", "src"))

# settings
TABLES: int = 5
CELLS: int = 1000
TOLERANCE = TABLES * CELLS * 10
CELLS_VALUE: str = "TEST"

database.config["DATABASE"]["AUTOLOAD"] = "No"


def check() -> bool:
    """Test the speed from foxy database sqlite3"""
    time_start = datetime.now()
    d = database.database(".test_object")

    for _ in range(TABLES):
        table = d.createTable()
        for i in range(CELLS):
            table.setCell("A"+str(i), CELLS_VALUE)

    d.save()

    final_time_foxy = datetime.now()-time_start

    import sqlite3

    time_start = datetime.now()
    database_sqlite = sqlite3.connect(":memory:")
    cursor = database_sqlite.cursor()

    for i in range(TABLES):
        cursor.execute("create table A"+str(i)+"(col text)")
        for j in range(CELLS):
            cursor.execute("insert into A"+str(i)+"(col)\nvalues("+str(j)+")")

    cursor.fetchall()
    final_time_sqlite = datetime.now()-time_start

    assert (final_time_foxy.microseconds -
            final_time_sqlite.microseconds) < TOLERANCE

    return True
