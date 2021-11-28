from os import getlogin
from foxy.database.database import *

d = database(".test_object")
excel = d.createTable("excel", excelParser)

excel.getCell("A1").setRawValue("=IF(AND('Doctor'='Doctorfuchs'; 3<4); 'IF/AND Success'; 'IF/AND Failed')")
excel.getCell("A2").setRawValue("=IF(OR('Doctor'='Doctorfuchs'; 3<4); 'IF/OR Success'; 'IF/OR Failed')")
excel.getCell("A3").setRawValue("=IF(SIN(0)=1; 'SIN Success'; 'SIN Failed')")

print(excel.getCells("A1:B3"))