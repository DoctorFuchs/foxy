import sqlite3
from foxy.database.table import Table   
from foxy.utils.publisher import Public

class Database:
    def __init__(self) -> None:
        self._tables = {}
        self._child = {}
    
    def _create_table(self, _table_name="", _import: Table=None):
        """Create a table in this database or import it from another database"""
        if _import == None:
            _import.master = self._get_public_database()
        else:
            _import = Table(master=self._get_public_database())
        
        if _table_name == "": _table_name = id(_import)
        self._tables[_table_name] = {
            "obj": _import,
            "name": _table_name
        }

    def _get_public_database(self):
        """get a Public_Database object, that you can use for apis to strangers"""
        return Public(self)

    def _get_sql_code(self):
        result = ""
        for table in self._tables:
            result += table.obj._get_sql_code().format(name=table.name)

    def _get_sqllite_database_mirror(self):
        sql_obj = sqlite3.connect(":memory:")
        sql_obj.executemany(self.get_sql_code())
        sql_obj.commit()

    def _open_console(self):
        pass
    