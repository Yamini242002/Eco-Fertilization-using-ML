import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")

# Open the .sql file and read the contents
with open("db.sql", "r") as f:
    sql = f.read()

# Execute the SQL commands
conn.executescript(sql)

# Save the changes
conn.commit()

# Close the connection
conn.close()
