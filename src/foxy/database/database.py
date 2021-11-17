import re
import pickle
import configparser as cp
import sys
import os
import threading
sys.path.append(__file__.replace(
    "foxy"+os.sep+"database"+os.sep+"database.py", ""))
from foxy.database.parser import *

class PatternDoesntMatch(BaseException):
    pass


class UnsupportedFileType(BaseException):
    pass


class tableNotFound(BaseException):
    pass


class FeatureInDevelopment(BaseException):
    pass


config = cp.ConfigParser()
config.read(__file__.replace("src"+os.sep+"foxy"+os.sep +
            "database"+os.sep+"database.py", "setup.cfg"))


class cell:
    def __init__(self, master_, pos_, value="") -> None:
        self.value = value
        self.raw = value
        self.pos = pos_
        self.master = master_
        self.master.cells[pos_] = self

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
            raise PatternDoesntMatch(config["ERRORS"]["Uppercase"])

        elif not re.match("[A-Z]+[0-9]+\:[A-Z]+[0-9]+$", pos_):
            raise PatternDoesntMatch(
                config["ERRORS"]["patternExampleMultipleCells"])

        # TODO getCells like in excel
        raise FeatureInDevelopment(
            "At the moment this functions is unvailable.")

    def getCell(self, pos_: str) -> cell:
        if not pos_.upper():
            raise PatternDoesntMatch(config["ERRORS"]["Uppercase"])

        elif not re.match("[A-Z]+[0-9]+$", pos_):
            raise PatternDoesntMatch(
                config["ERRORS"]["patternExampleSingleCell"])

        if pos_ in self.cells:
            return self.cells[pos_]

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

        if config["DATABASE"]["autosave"] == "Yes":
            import threading
            savethread = threading.Thread(target=self.saveforever)
            savethread.setDaemon(True)
            savethread.start()

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
            raise tableNotFound(config["ERRORS"]["tableNotFound"])

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
