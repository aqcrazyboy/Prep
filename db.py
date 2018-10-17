import sqlite3

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class DB(object):
    def __init__(self):
        self.conn = sqlite3.connect("test.db") #check_same_thread?
        self.createtable()

    def createtable(self):
        try:
            self.conn.execute("""
                CREATE TABLE test (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    userid INTEGER UNIQUE NOT NULL,
                    rating INTEGER CHECK(0 <= rating <= 10),
                    chekintime DEFAULT CURRENT_TIME  NOT NULL
                    );
            """)
        except Exception as e:
            print(e)

    def insert(self, userid, rating):
        cursor = self.conn.execute("""
            INSERT INTO test (userid, rating) VALUES (?,?);
        """, (userid, rating))
        self.conn.commit()
        return {'id':row[0], 'userid':row[1], 'rating':row[2],
        'checkintime':row[3]}

    def getID(self, id):
        cursor = self.conn.execute("SELECT * FROM test WHERE id == ?", (id,))
        for row in cursor:
            return {'id':row[0], 'userid':row[1], 'rating':row[2],
            'checkintime':row[3]}

    def updateTask(self, id, rating):
        cursor = self.conn.execute("UPDATE test SET rating = ? WHERE id = ?",
        (rating, id))
        self.conn.commit()
        for row in cursor:
            return {'id':row[0], 'userid':[1], 'rating':row[2],
            'checkintime':row[3]}

    def deleteTask(self, id):
        self.conn.execute("DELETE FROM test)

    def getAll(self):
        cursor = self.conn.execute("SELECT * FROM test;")
        table = []

        for row in cursor:
            table.append({'id': row[0], 'user': row[1], 'rating': row[2],
            'checkintime':row[3]})
        return table

DB = singleton(DB)
