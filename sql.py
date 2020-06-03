import sqlite3
#from pysqlcipher import dbapi2 as sqlcipher

conn = sqlite3.connect('test.db')
#db = sqlcipher.connect('test.db')

conn.execute('pragma key="password"')
print ("Opened database successfully")

conn.execute('''CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);''')

print ("Table created successfully")

db.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Simon', 1422, 'California', 100000.00 )");


conn.commit()
print ("Records created successfully")
conn.close()

#from pycipher import dbapi2 as sqlite
#conn = sqlite.connect('test.db')
#c = conn.cursor()
#c.execute("PRAGMA key='password'")
#c.execute('''create table stocks (date text, trans text, symbol text, qty real, price real)''')
#c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
#conn.commit()
#c.close()