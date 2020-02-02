import sqlite3  
  
con = sqlite3.connect("myDB2.db")  
print("Database opened successfully")  
  
con.execute("create table myTable (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER)")  
  
print("Table created successfully")  
  
con.close()  