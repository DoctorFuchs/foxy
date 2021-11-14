import sys
import os
import time
sys.path.append(__file__.replace("tests"+os.sep+"benchmarks"+os.sep+"save.py", "src"))
from foxy.database import database 

database.config["DATABASE"]["AUTOLOAD"] = "No"

def check() -> bool:
    """Check save and load function"""
    databaseIn = database.database(".data")
    databaseIn.createTable("test_table").setCell("A1", "PING")
    databaseIn.save()
    time.sleep(1) # need to sleep, because to save the database is in a thread (for more speed)
    databaseOut = database.database(".data")
    databaseOut.load()
    assert databaseOut.getTable("test_table").getCell("A1").getValue() == "PING"
    return True
    
if __name__ == "__main__":
    check()