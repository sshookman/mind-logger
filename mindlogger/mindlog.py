from datetime import datetime

class mindlog():
    timestamp = None
    task = None
    message = None

    def __init__(self, message, task=None):
        if not task:
            task = None
        else:
            task = task.replace("'", "''")

        self.timestamp = datetime.now().strftime("[%Y/%m/%d %H:%M:%S]")
        self.message = message.replace("'", "''")
        self.task = task
