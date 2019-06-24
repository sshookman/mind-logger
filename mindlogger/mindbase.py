import sqlite3
import os

from .mindlog import mindlog
from .renderer import Renderer
from .styles import color_codes

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

    def show(self, query="SELECT * FROM mindlog ORDER BY date DESC LIMIT 100", active_task="None"):
        rows = []
        for row in self.cursor.execute(query):
            rows.append(row)

        # Should be located outside of this class
        task_stamp_color = color_codes["cyan"] + color_codes["bold"]
        date_stamp_color = color_codes["bg-light-cyan"] + color_codes["bold"]
        snip_stamp_color = color_codes["bg-white"] + color_codes["black"] + color_codes["bold"]
        activ_stamp_color = color_codes["bg-white"] + color_codes["black"] + color_codes["bold"]
        code_block_color = color_codes["bg-white"] + color_codes["black"] + color_codes["bold"]
        renderer = Renderer(task_stamp_color, date_stamp_color, snip_stamp_color, activ_stamp_color, code_block_color)
        renderer.render_rows(rows, active_task=active_task)

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
