import sqlite3 as sl
import os.path


class db:
    def __init__(self, table):
        self.table = table
        if os.path.isfile('main.db') == False:
            self.con = sl.connect('main.db')
            with self.con:
                self.con.execute("""
                    CREATE TABLE meetData (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                        
                    visited TEXT,
                    parentID INTEGER,
                    subject TEXT,
                    link TEXT,
                    timeForMeet TEXT
                    );
                """)
            with self.con:
                self.con.execute("""
                    CREATE TABLE msgData (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    msg TEXT,
                    timeSent TEXT,                    
                    sentGroup TEXT,
                    msgRead TEXT,
                    hash TEXT
                    );
                """)
        else:
            self.con = sl.connect('main.db')

    def insert(self, data, returnID = False):
        if self.table == "meetData":
            sql = 'INSERT INTO '+self.table+' (link, timeForMeet, subject, parentID, visited) values(?, ?, ?, ?, ?)'            
            with self.con:
                self.con.executemany(sql, data)
            id = self.get("parentID", data[0][3])[0][0]
        elif self.table == "msgData":
            sql = 'INSERT INTO '+self.table+' (msg, timeSent, sentGroup, msgRead, hash) values(?, ?, ?, ?, ?)'            
            with self.con:
                self.con.executemany(sql, data)            
            id = self.get("timeSent", data[0][1])[0][0]
        if(returnID):
            return id

    def get(self, field, value):
        with self.con:
            data = self.con.execute("SELECT * FROM "+self.table+" WHERE "+ str(field) +" == '" + str(value) + "'")
            return data.fetchall()

    def getAll(self):
        with self.con:
            data = self.con.execute("SELECT * FROM " + self.table)
            return data.fetchall()

    def update(self, id, data=[]):
        if len(data) < 1:
            sql = "UPDATE "+self.table+" SET visited = 'True' WHERE id = " + str(id)
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
        else: 
            for i in data:
                sql = "UPDATE "+self.table+" SET " + str(i) + " = '" + str(data[i]) + "' WHERE id = " + str(id)
                cur = self.con.cursor()
                cur.execute(sql)
                self.con.commit()

    def delete(self, id):    
        sql = 'DELETE FROM '+self.table+' WHERE id=?'
        cur = self.con.cursor()
        cur.execute(sql, (id,))
        self.con.commit()