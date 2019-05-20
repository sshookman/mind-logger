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

    def show(self, query="SELECT * FROM mindlog ORDER BY date DESC LIMIT 100", activeTask="None"):
        #TODO: This should be configurable by the user and placed in a config somewhere
        activeTaskColor="\033[0m\033[36m\033[1m"
        dateColor="\033[0m\033[44m\033[1m"
        endColor="\033[0m"

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
                print("\n{col}                              {date}                              {end}".format(date=date, col=dateColor, end=endColor))
            if (task != row[1]):
                task = row[1]
                if (task == "None"):
                    print("\n")
                else:
                    col = activeTaskColor if activeTask == task else endColor
                    print("\n{col}_____{task}_____".format(task=task, col=col))
                
            print(row[0], " | ", row[2])
        print(endColor)

    def search(self, context):
        query = "SELECT * FROM mindlog{where} ORDER BY date DESC"
        where = ""
        tokens = context.split(" ")

        raw = ""
        prevToken = ""
        for idx, token in enumerate(tokens):
            if (token == "-t"):
                task = tokens[idx+1]
                where = " WHERE" if where == "" else "{where} AND".format(where=where)
                where = "{where} task = '{task}'".format(where=where, task=task)
            elif (token == "-d"):
                date = tokens[idx+1].replace("-", "/")
                where = " WHERE" if where == "" else "{where} AND".format(where=where)
                where = "{where} date LIKE '%{date}%'".format(where=where, date=date)
            elif (prevToken.startswith("-") == False):
                raw = "{raw}{token} ".format(raw=raw, token=tokens[idx])
            prevToken = token

        where = " WHERE" if where == "" else "{where} AND".format(where=where)
        where = "{where} message LIKE '%{raw}%'".format(where=where, raw=raw.strip())
        query = query.format(where=where)

        self.show(query)
        print(query)
        input("\n[PRESS ENTER TO CONTINUE]")


    def close(self):
        self.conn.close()
