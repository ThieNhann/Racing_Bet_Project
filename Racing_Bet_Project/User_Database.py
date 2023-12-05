import sqlite3
import hashlib

conn = sqlite3.connect('database/User_Data.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS User_Data(
            User_ID INTEGER PRIMARY KEY,
            Username VAR CHAR(255) NOT NULL,
            Password VAR CHAR(255) NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS User_History(
            History_ID INTEGER PRIMARY KEY,
            USER_ID INTEGER,
            SELECTED_CHAR VAR CHAR(255),
            RESULT VAR CHAR(255),
            FOREIGN KEY(USER_ID) REFERENCES User_Data(User_ID)
)
""")
password = hashlib.sha256('12345'.encode()).hexdigest()
#cur.execute("INSERT INTO User_Data(Username, Password) VALUES (?,?)", ('nnkhang2005@gmail.com', password))

cur.execute("SELECT * FROM User_Data")
#print(cur.fetchall())

conn.commit()



