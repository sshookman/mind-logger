import datetime

class mindlog():
    timestamp = None
    task = None
    message = None

    def __init__(self, message, task=None):
        if not task:
            task = None

        self.timestamp = datetime.datetime.now().strftime("[%Y/%m/%d %H:%M]")
        self.task = task
        self.message = message
