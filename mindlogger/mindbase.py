import sqlite3
import os

from .mindlog import mindlog

class mindbase():
    conn = None
    cursor = None
    
    def __init__(self, mind="mindlogger"):
        path = "{mind}.mldb".format(mind=mind)
        exists = os.path.isfile(path)
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        if (exists == False):
            self.cursor.execute("CREATE TABLE mindlog (date text, task text, message text)")
            self.conn.commit()

    def log(self, log):
        timestamp = log.timestamp
        task = log.task
        message = log.message
        insert = "INSERT INTO mindlog VALUES ('{timestamp}', '{task}', '{message}')"
        insert = insert.format(timestamp=log.timestamp, task=log.task, message=log.message)
        self.cursor.execute(insert)
        self.conn.commit()

    def show(self):
        print('\x1bc')
        task = "None"
        for row in self.cursor.execute("SELECT * FROM mindlog"):
            if (task != row[1]):
                task = row[1]
                if (task == "None"):
                    print("\n")
                else:
                    print("\n_____{task}_____".format(task=task))
                
            print(row[0], " | ", row[2])


    def close(self):
        self.conn.close()
