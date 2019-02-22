###############################################
#                 MIND LOGGER                 #
#---------------------------------------------#
# Command-line REPL to log the thoughts from  #
# your brain in an organized easy to access   #
# structure.                                  #
###############################################

import argparse

from .mindlog import mindlog
from .mindbase import mindbase

def main():
    parser = argparse.ArgumentParser(description='FEAR... IS... THE MIND LOGGER')
    parser.add_argument('-m', '--mind', help="The name of the mindlogger output file", default="mind")
    args = parser.parse_args()
    mldb = mindbase(args.mind)
    mldb.show()

    message = None
    task = ""
    while (message != "\exit"):
        message= input("\n{task} > ".format(task=task))

        if (message.startswith("\\") == False):
            log = mindlog(message, task)
            mldb.log(log)
        elif (message.startswith("\\task")):
            task = message.replace("\\task", "").strip()
        elif (message.startswith("\\search")):
            search = message.replace("\\search", "").strip()
            mldb.search(search)

        mldb.show()

    mldb.close()
