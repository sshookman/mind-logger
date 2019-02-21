from datetime import datetime

class mindlog():
    timestamp = None
    task = None
    message = None

    def __init__(self, message, task=None):
        if not task:
            task = None

        self.timestamp = datetime.now().strftime("[%Y/%m/%d %H:%M]")
        self.task = task
        self.message = message

        # TODO: Need to find a way to escape special characters or sanitize the input somehow
