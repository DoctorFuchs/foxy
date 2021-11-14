from database import  database as db
from database.parser import excelParser

johannes = db.database("johannes")
j = johannes.createTable("Hallo", parser_=excelParser)
j = johannes.getTable("Hallo")
#j.getCell("B2").setRawValue("=SIN(1)")
#j.getCell("A1").setRawValue("=MAX(B2, 0)")

print(j.getCell("A1").getValue())

j.getCell("A1").setRawValue("=0.1+0.2")
print(j.getCell("A1").getValue())
johannes.save()