import mysql.connector as con

db = con.connect(
  host = 'localhost',
  username = 'root',
  password = '',
  database = 'testdb'
)

cur = db.cursor()