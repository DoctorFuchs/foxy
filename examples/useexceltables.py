# Attention! The excel-parser is not finished yet. There are only some math functions
from foxy.database import database

yourDatabase = database.database("your_database_name")
yourTable = yourDatabase.createTable("A table name")

# now use your table for whatever

# don't forget to save the database
yourDatabase.save()
