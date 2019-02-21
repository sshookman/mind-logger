import sqlite3
import os

from datetime import datetime

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
        date = ""
        for row in self.cursor.execute("SELECT * FROM mindlog ORDER BY date ASC"):
            latestDate = datetime.strptime(row[0], "[%Y/%m/%d %H:%M]").date()
            if (date != latestDate):
                date = latestDate
                task = "None"
                print("\n_______________{date}_______________".format(date=date))
            if (task != row[1]):
                task = row[1]
                if (task == "None"):
                    print("\n")
                else:
                    print("\n_____{task}_____".format(task=task))
                
            print(row[0], " | ", row[2])


    def close(self):
        self.conn.close()
