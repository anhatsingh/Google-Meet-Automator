import sqlite3 as sl
import os.path


def doOnce():
    if os.path.isfile('database.db') == False:
        con = sl.connect('database.db')
        with con:
            con.execute("""
                CREATE TABLE meetData (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                        
                visited TEXT,
                parentID INTEGER,
                subject TEXT,
                link TEXT,
                timeForMeet TEXT
                );
            """)
        with con:
            con.execute("""
                CREATE TABLE msgData (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                msg TEXT,
                timeSent TEXT,                    
                sentGroup TEXT,
                msgRead TEXT,
                hash TEXT
                );
            """)

    if os.path.isfile('config.db') == False:
        with sl.connect('config.db') as con2:
            con2.execute("""
                CREATE TABLE configData (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                        
                theField TEXT,
                theValue TEXT,
                other TEXT
                );
            """)
            con2.execute("""
                CREATE TABLE wa_groups (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                        
                name TEXT
                );
            """)
            con2.executemany("INSERT INTO configData (theField, theValue, other) values(?, ?, ?)", [
                ("min_meet_parti", "20", "meet"),
                ("logout_checker_time", "900", "meet"),
                ("record_meetings", "1", "obs"),
                ("location_to_obs_shortcut", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OBS Studio\\OBS Studio (64bit).lnk", "obs"),
                ("video_save_location", "E:\\AnhatUser\\Videos\\", "obs"),
                ("username", "", "google"),
                ("password", "", "google"),
                ])
            con2.execute("INSERT INTO wa_groups (name) values('Automation')")


class db:
    def __init__(self, table):
        self.table = table        

    def insert(self, data, returnID = False):
        if self.table == "meetData":
            sql = 'INSERT INTO '+self.table+' (link, timeForMeet, subject, parentID, visited) values(?, ?, ?, ?, ?)'                        
            with sl.connect("database.db") as con:
                con.executemany(sql, data)            
            id = self.get("parentID", data[0][3])[0][0]

        elif self.table == "msgData":
            sql = 'INSERT INTO '+self.table+' (msg, timeSent, sentGroup, msgRead, hash) values(?, ?, ?, ?, ?)'            
            with sl.connect("database.db") as con:
                con.executemany(sql, data)            

            id = self.get("timeSent", data[0][1])[0][0]
        if(returnID):
            return id

    def get(self, field, value):
        with sl.connect("database.db") as con:
            data = con.execute("SELECT * FROM "+self.table+" WHERE "+ str(field) +" == '" + str(value) + "'")
            return data.fetchall()

    def getAll(self):
        with sl.connect("database.db") as con:
            data = con.execute("SELECT * FROM " + self.table)
            return data.fetchall()

    def update(self, id, data=[], state = "True"):
        if len(data) < 1:
            sql = "UPDATE "+self.table+" SET visited = '" +str (state) + "' WHERE id = " + str(id)
            with sl.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(sql)
                con.commit()
        else: 
            for i in data:
                sql = "UPDATE "+self.table+" SET " + str(i) + " = '" + str(data[i]) + "' WHERE id = " + str(id)
                with sl.connect("database.db") as con:
                    cur = con.cursor()
                    cur.execute(sql)
                    con.commit()

    def delete(self, id):    
        sql = 'DELETE FROM '+self.table+' WHERE id=?'        
        with sl.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(sql, (id,))
            con.commit()

    def updateTime(self, newTime, id):
        sql = "UPDATE " + self.table + " SET timeForMeet = '" + str(newTime) + "' WHERE id = " + str(id)
        with sl.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
        
        sql = "UPDATE " + self.table + " SET visited = 'False' WHERE id = " + str(id)
        with sl.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(sql)
            con.commit()

    def updateParent(self, oldID, newID):
        sql = "UPDATE " + self.table + " SET parentID = ? WHERE id = ?"        
        with sl.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(sql, (newID, oldID,))
            con.commit()


class config:
    def __init__(self, table):
        self.table = table
    
    def get(self, field, value):
        with sl.connect("config.db") as con:
            data = con.execute("SELECT * FROM "+self.table+" WHERE "+ str(field) +" == '" + str(value) + "'")
            return data.fetchall()

    def getAll(self):
        with sl.connect("config.db") as con:
            data = con.execute("SELECT * FROM " + self.table)
            return data.fetchall()
    
    def delete(self, id):    
        sql = 'DELETE FROM '+self.table+' WHERE id=?'        
        with sl.connect("config.db") as con:
            cur = con.cursor()
            cur.execute(sql, (id,))
            con.commit()

    def insert(self, data):        
        if(self.table == "configData"):
            sql = 'INSERT INTO configData (theField, theValue, other) values(?, ?, ?)'                        
        else:
            sql = 'INSERT INTO wa_groups (name) values(?)'
        
        with sl.connect("config.db") as con:
            con.executemany(sql, data)                    
    
    def update(self, field, value, whereField, whereValue):                
        sql = "UPDATE "+ self.table +" SET " + str(field) + " = '" + str(value) + "' WHERE " + str(whereField) + " = '" + str(whereValue) + "'"
        with sl.connect("config.db") as con:
            cur = con.cursor()
            cur.execute(sql)
            con.commit()