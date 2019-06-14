from datetime import datetime
from .styles import color_codes

CLEAR = color_codes["clear"]
RESET = color_codes["reset"]
ENDL  = "\n"

DATE_STAMP = "\n{col}                              {date}                              {end}"
TASK_STAMP = "\n{col}_____{task}_____"
LOG_STAMP  = "{date} | {message}"

DATE_FORMAT = "[%Y/%m/%d %H:%M:%S]"

SNIPPET_CHAR  = "`"
SNIPPET_STAMP = "{reset}{col}"

class Renderer():
    c_task_stamp = ""
    c_date_stamp = ""
    c_snip_stamp = ""

    def __init__(self,  task_stamp_color="", date_stamp_color="", snip_stamp_color=""):
        self.c_task_stamp = task_stamp_color
        self.c_date_stamp = date_stamp_color
        self.c_snip_stamp = snip_stamp_color

    def render_rows(self, rows, task=None, date=None, active_task=None):
        # Clear screen, and display the rows (oldest to newest)
        print(CLEAR)
        for row in reversed(rows):
            # Obtain row values
            date_time = row[0]
            task_name = row[1]
            message  = row[2]

            # Print the date if it has changed
            latestDate = datetime.strptime(date_time, DATE_FORMAT).date()
            if (date != latestDate):
                date = latestDate
                task = None
                print(DATE_STAMP.format(date=date, col=self.c_date_stamp, end=RESET))

            # Update the task, color, and display the name if it has changed
            if (task != task_name):
                task = task_name
                if (task is None) | (task == "None"):
                    self._endl()
                else:
                    col = RESET + self.c_task_stamp if active_task == task else RESET
                    print(TASK_STAMP.format(task=task, col=col))

            # Print the log for the given row
            print(LOG_STAMP.format(date=date_time, message=self._format_message(message, col)))

        self._reset()

    def _format_message(self, message, col=""):
        while (message.count(SNIPPET_CHAR) >= 2):
            message = message.replace(SNIPPET_CHAR, SNIPPET_STAMP.format(reset=RESET, col=self.c_snip_stamp), 1)
            message = message.replace(SNIPPET_CHAR, SNIPPET_STAMP.format(reset=RESET, col=col), 1)

        return message

    def _reset(self):
        print(RESET)

    def _endl(self):
        print(ENDL)
