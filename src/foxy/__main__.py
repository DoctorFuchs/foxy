from database import  database as db
from database.parser import excelParser

johannes = db.database("johannes")
j = johannes.createTable("Hallo", parser_=excelParser)
j = johannes.getTable("Hallo")
#j.getCell("B2").setRawValue("=SIN(1)")
#j.getCell("A1").setRawValue("=MAX(B2, 0)")

j.getCell("B2").setRawValue("=MAX(90, 180)")
j.getCell("C2").setRawValue("=MAX(10, 80)")
j.getCell("A1").setRawValue("=PRODUCT(B2, C2)")
print(j.getCell("A1").getValue())
print(j.getCell("B2").getValue())
johannes.save()