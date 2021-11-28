from foxy.database.database import *

josh = database("josh")

josh_friends = josh.createTable("friends", excelParser)
josh_friends.getCell("PAUL1").setValue("Timon")
josh_friends.getCell("PAUL2").setRawValue("=IF(PAUL1='Paul'; 'Johannes'; 'Jakob')")

print(josh_friends.getCell("PAUL1").value)
print(josh_friends.getCell("PAUL2").value)

