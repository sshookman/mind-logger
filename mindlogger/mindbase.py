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

    def show(self, query="SELECT * FROM mindlog ORDER BY date DESC LIMIT 100"):
        print('\x1bc')
        task = "None"
        date = ""
        rows = []
        for row in self.cursor.execute(query):
            rows.append(row)
        for row in reversed(rows):
            latestDate = datetime.strptime(row[0], "[%Y/%m/%d %H:%M:%S]").date()
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

    def search(self, context):
        query = "SELECT * FROM mindlog{where} ORDER BY date DESC"
        where = ""
        tokens = context.split(" ")

        for idx, token in enumerate(tokens):
            if (token == "-t"):
                task = tokens[idx+1]
                where = " WHERE" if where == "" else "{where} AND".format(where=where)
                where = "{where} task = '{task}'".format(where=where, task=task)
            if (token == "-d"):
                date = tokens[idx+1].replace("-", "/")
                where = " WHERE" if where == "" else "{where} AND".format(where=where)
                where = "{where} date LIKE '%{date}%'".format(where=where, date=date)

        query = query.format(where=where)

        self.show(query)
        input("\n[PRESS ENTER TO CONTINUE]")


    def close(self):
        self.conn.close()
