import sys
sys.path.append("D:\\Paul\\Projekte\\Python\\foxy\\src")

import foxy.debugger
from foxy.database.cell import Cell

c = Cell("123")
c.pos = "123412"
print(c.pos)