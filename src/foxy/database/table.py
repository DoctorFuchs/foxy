from foxy.database.cell import Cell

class Table:
    def __init__(self, _master) -> None:
        self._master = _master
        self._cells = {}

    def _get_sql_code(self) -> str:
        result = ""
        # create
        result += "create table {name} {\ncell_pos text(2) not null unique,\ncell_value longtext,\ncell_raw_value longtext\n}"
        # insert into
        result += "INSERT INTO {name} (cell_pos,cell_value,cell_raw_value)\nVALUES\n"
        for cell in self._cells:
            result += f"({cell.pos}, {cell.value}, {cell.raw_value}),\n"
        # end
        result += ";"
        return result
    
    def _add_cell(self, cell: Cell):
        self._cells[cell.pos] = cell
    
    def _create_cell(self, pos, value="", raw_value=""):
        self._cells[pos] = Cell(pos, value, raw_value)
