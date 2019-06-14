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
        rows = []
        for row in self.cursor.execute(query):
            rows.append(row)

        self.displayLog(rows, "None", "", activeTask)

    def displayLog(self, rows, task, date, activeTask):
        #TODO: This should be configurable by the user and placed in a config somewhere
        activeTaskColor="\033[0m\033[36m\033[1m"
        dateColor="\033[0m\033[44m\033[1m"
        endColor="\033[0m"

        # Clear screen, and display logs row by row (oldest to newest)
        print('\x1bc')
        for row in reversed(rows):
            # Obtain row values
            date_time = row[0]
            task_name = row[1]
            message  = row[2]

            # Print the date if it has changed
            latestDate = datetime.strptime(date_time, "[%Y/%m/%d %H:%M:%S]").date()
            if (date != latestDate):
                date = latestDate
                task = "None"
                print("\n{col}                              {date}                              {end}".format(date=date, col=dateColor, end=endColor))

            # Update the task, color, and display the name if it has changed
            if (task != task_name):
                task = task_name
                if (task == "None"):
                    print("\n")
                else:
                    col = activeTaskColor if activeTask == task else endColor
                    print("\n{col}_____{task}_____".format(task=task, col=col))

            # Print the log
            print(date_time, "|", self.formatMessage(message, col))

        print(endColor)

    def formatMessage(self, message, col=""):
        # Replace sections of `code` with proper highlighting
        snippet_char = "`"
        while (message.count(snippet_char) >= 2):
            message = message.replace(snippet_char, "\033[0m\033[107m\033[30m ", 1)
            message = message.replace(snippet_char, " \033[0m{col}".format(col=col), 1)

        return message

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
