from foxy.database import database

yourDatabase = database.database("your_database_name")
yourTable = yourDatabase.createTable("A database name")

# now use your table for whatever