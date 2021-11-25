import pickle
import re
import os
import threading
from typing import DefaultDict, Union
from foxy.database.parser import *

class PatternDoesntMatch(BaseException):
    pass


class UnsupportedFileType(BaseException):
    pass


class tableNotFound(BaseException):
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
        raise PatternDoesntMatch("Please use a pattern like A1 or Doctor11")
    

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

    def getCells(self, pos_):
        if not pos_.upper():
            raise PatternDoesntMatch("Position must be uppercase")

        elif not re.match("[A-Z]+[0-9]+\:[A-Z]+[0-9]+$", pos_):
            raise PatternDoesntMatch("Please use a pattern like A1:C3 or MOVIES1:Series9")

        # TODO getCells like in excel
        raise FeatureInDevelopment(
            "At the moment this functions is unvailable.")

    def getCell(self, pos_: str) -> cell:
        if not pos_.upper():
            raise PatternDoesntMatch("Position must be uppercase")

        elif not re.match("[A-Z]+[0-9]+$", pos_):
            raise PatternDoesntMatch("Please use a pattern like A1 or Doctor11")

        if pos_ in self.cells:
            pos = splitPos(pos_)
            return self.cells[pos[0]][pos[1]]

        else:
            return cell(self, pos_, "")

    def setCell(self, pos_, value):
        self.getCell(pos_).setValue(value)

    def __str__(self) -> str:
        return str(self.cells)


class database:
    def __init__(self, name_="database$id") -> None:
        self.name = name_.replace("$id", str(id(self)))
        self.DatabaseFileType = config["DATABASE"]["filetype"]
        self.tables = {}
        self.filepath = self.name+self.DatabaseFileType
        
        if config["DATABASE"]["autoload"] == "Yes":
            self.load()

    def __sizeof__(self) -> int:
        return os.path.getsize(self.filepath)

    def save(self):
        file = open(self.name+self.DatabaseFileType, "w+b")
        def dump(): pickle.dump(self, file, protocol=pickle.HIGHEST_PROTOCOL); file.close()
        threading.Thread(target=dump).start()

    def load(self):
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
