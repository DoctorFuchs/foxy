import pickle
import re
import os
import threading
from typing import DefaultDict, Union
from typing_extensions import final
from foxy.database.parser import *

class PatternDoesntMatch(BaseException):
    pass


class UnsupportedFileType(BaseException):
    pass


class tableNotFound(BaseException):
    pass


class databaseNotFound(BaseException):
    pass


class FeatureInDevelopment(BaseException):
    pass


config = {
    "DATABASE":{
        "autoload": "Yes",
        "autosave": "No", # in production
        "filetype": ".foxydb"
    }
}


def splitPos(pos_: str) -> Union[str, str]:
    import re
    match = re.match(r"([A-Za-z]+)([0-9]+)", pos_, re.I)
    if match:
        return match.groups()
    
    else:
        raise PatternDoesntMatch("Please use a pattern like A1 or DOCTOR11")
    

class cell:
    def __init__(self, master_, pos_, value="") -> None:
        self.value = value
        self.raw = value
        self.pos = pos_
        self.master = master_
        if self.master.cells.get(splitPos(pos_)[0]) == None: self.master.cells[splitPos(pos_)[0]]={}
        self.master.cells[splitPos(pos_)[0]][splitPos(pos_)[1]] = self

    def getValue(self):
        return self.value

    def setValue(self, newvalue_, handle_=True):
        self.value = newvalue_
        if handle_:
            self.master.parser.__beforeHandle__(self)

    def setRawValue(self, newvalue_, handle_=True):
        self.raw = newvalue_
        if handle_:
            self.master.parser.__beforeHandle__(self)

    def getRawValue(self):
        return self.raw

    def __call__(self, *args, **kwds) -> str:
        return self.value

    def write(self, value_):
        self.setValue(value_, handle_=False)


class table:
    def __init__(self, master_, name_: str = "table$id", import_=None, parser_=defaultParser) -> None:
        """create a table
        :param master_ : a database instance
        :param import_: a table from another database"""
        if import_:
            self = import_
        self.master = master_
        self.name = name_.replace("$id", str(id(self)))
        
        self.cells = {}
        self.master.tables[self.name] = self
        self.parser = parser_(self)

    def getCells(self, pos_: str):
        if not pos_.upper():
            raise PatternDoesntMatch("Position must be uppercase")

        elif not re.match("[A-Z]+[0-9]+\:[A-Z]+[0-9]+$", pos_):
            raise PatternDoesntMatch("Please use a pattern like A1:C3 or MOVIES1:SERIES9")
        
        final = []
        pos = pos_.split(":")
        for pos_char in range(ord(splitPos(pos[0])[0]), ord(splitPos(pos[1])[0])):
            print("char: "+pos_char)
            for pos_num in range(int(splitPos(pos[0])[1]), int(splitPos(pos[1])[1])):
                final.append(self.getCell(chr(pos_char)+pos_num))

        return final

    def getCell(self, pos_: str) -> cell:
        if not pos_.upper():
            raise PatternDoesntMatch("Position must be uppercase")

        elif not re.match("[A-Z]+[0-9]+$", pos_):
            raise PatternDoesntMatch("Please use a pattern like A1 or DOCTOR11")

        pos = splitPos(pos_)
        try:
            return self.cells[pos[0]][pos[1]]

        except KeyError:
            return cell(self, pos_, "")

    def setCell(self, pos_, value):
        self.getCell(pos_).setRawValue(value)
        return self.getCell(pos_)

    def __str__(self) -> str:
        return str(self.cells)


class database:
    def __init__(self, name_="database$id", master_=None, import_=None) -> None:
        if import_ != None:
            self = import_
        
        else:
            self.name = name_.replace("$id", str(id(self)))
            self.DatabaseFileType = config["DATABASE"]["filetype"]
            self.tables = {}
            self.databases = {}
        
        self.filepath = self.name+self.DatabaseFileType
        self.master = master_

        if self.master != None:
            self.master.databases[self.name] = self
        
        if config["DATABASE"]["autoload"] == "Yes":
            self.load()

    def __sizeof__(self) -> int:
        return os.path.getsize(self.filepath)

    def isChild(self):
        return False if self.master_ == None else True

    def save(self):
        if self.isChild(): return
        file = open(self.name+self.DatabaseFileType, "w+b")
        def dump(): pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL); file.close()
        threading.Thread(target=dump).start()

    def load(self):
        if self.isChild(): return
        try:
            file = open(self.name+self.DatabaseFileType, "rb")
            pickleLoader = pickle.load(file)
            self.tables = pickleLoader.tables

        except (EOFError, OSError):
            pass

        except FileNotFoundError:
            # suggestion from DoctorFuchs: print("You need to save your database before loading")
            pass

        finally:
            try:
                file.close()
            except:
                pass

    def getTable(self, name_: str) -> table:
        try:
            return self.tables[name_]

        except KeyError:
            raise tableNotFound("No table found in this database")
    

    def deleteTable(self, name_: str) -> table:
        try:
            del self.tables[name_]

        except KeyError:
            raise tableNotFound("No table found in this database")

    def createTable(self, name=None, parser_=defaultParser):
        if name is None:
            return table(master_=self, parser_=parser_)

        else:
            if name in self.tables:
                return self.getTable(name)
            else:
                return table(master_=self, name_=name, parser_=parser_)

    def importTable(self, table_: table):
        return table(master_=self, import_=table_)

    def createDatabase(self, name_=None):
        return database(self.name+".child" if name_ == None else name_+len(self.databases), master_=self)
        
    def importDatabase(self, database_):
        assert type(database_) != type(self), "database parameter is not a database"
        return database(import_=database_)
    
    def getDatabase(self, name_):
        try:
            return self.databases[name_]

        except KeyError:
            raise databaseNotFound("No database found in this database")
    
    def deleteDatabase(self, name_):
        try:
            del self.databases[name_]

        except KeyError:
            raise databaseNotFound("No database found in this database")
