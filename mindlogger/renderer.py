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
    c_activ_snip = ""
    c_code_block = ""

    def __init__(self,  task_stamp_color="", date_stamp_color="", snip_stamp_color="", activ_snip_color="", code_block_color=""):
        self.c_task_stamp = task_stamp_color
        self.c_date_stamp = date_stamp_color
        self.c_snip_stamp = snip_stamp_color
        self.c_activ_snip = activ_snip_color
        self.c_code_block = code_block_color

    def render_rows(self, rows, task=None, date=None, active_task=None):
        col = ""
        snip_col = self.c_snip_stamp
        code_block_active = False

        # Clear screen, and display the rows (oldest to newest)
        row_num = 0
        print(CLEAR)
        for row in reversed(rows):
            # Obtain row values
            date_time = row[0]
            task_name = row[1]
            message  = row[2]

            # Print the date if it has changed
            latestDate = datetime.strptime(date_time, DATE_FORMAT).date()
            if (date != latestDate):
                code_block_active = False
                date = latestDate
                task = None
                print(DATE_STAMP.format(date=date, col=self.c_date_stamp, end=RESET))

            # Update the task, color, and display the name if it has changed
            if (task != task_name):
                code_block_active = False
                task = task_name
                if (task is None) | (task == "None"):
                    print(RESET)
                    snip_col = RESET + self.c_snip_stamp
                else:
                    col = RESET + self.c_task_stamp if active_task == task else RESET
                    snip_col = RESET + self.c_activ_snip if active_task == task else RESET + self.c_snip_stamp
                    print(TASK_STAMP.format(task=task, col=col))

            # Print the log for the given row or toggle code block
            if (message == "```"):
                if (code_block_active):
                    # de-activate
                    row_num = 0
                    code_block_active = False
                else:
                    # activate
                    row_num = 1
                    code_block_active = True
            else:
                print(LOG_STAMP.format(date=date_time, message=self._format_message(message, col, snip_col, code_block_active, row_num)))
                if (row_num > 0):
                    row_num += 1

        self._reset()

    def _format_message(self, message, col="", snip_col="", code_block_active=False, row=0):
        if (code_block_active):
            message = self.c_code_block + str(row) + " | " + message + RESET + col
        else:
            while (message.count(SNIPPET_CHAR) >= 2):
                message = message.replace(SNIPPET_CHAR, SNIPPET_STAMP.format(reset=RESET, col=snip_col), 1)
                message = message.replace(SNIPPET_CHAR, SNIPPET_STAMP.format(reset=RESET, col=col), 1)

        return message

    def _reset(self):
        print(RESET)
