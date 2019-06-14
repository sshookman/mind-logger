###############################################################
#                        MIND LOGGER                          #
#-------------------------------------------------------------#
# Command-line REPL to log the thoughts from your brain in an #  
# organized, easily accessible structure.                     #
###############################################################

import argparse

from .mindlog import mindlog
from .mindbase import mindbase
from .config import config

def main():
    parser = argparse.ArgumentParser(description='FEAR... IS... THE MIND LOGGER')
    parser.add_argument('-m', '--mind', help="The name of the mindlogger output file", default="mind")
    args = parser.parse_args()
    mldb = mindbase(args.mind)
    mldb.show()

    message = None
    task = ""
    while (message != "\exit"):
        message= input("\n\033[44m\033[1m[ {task} ]\033[0m\033[97m ".format(task=task))
        print("\033[0m")

        if (message.startswith("\\") == False):
            log = mindlog(message, task)
            mldb.log(log)
        elif (message.startswith("\\task")):
            task = message.replace("\\task", "").strip()
        elif (message.startswith("\\search")):
            search = message.replace("\\search", "").strip()
            mldb.search(search)

        mldb.show(active_task=task)

    mldb.close()
