Mind Logger
---
Command-line REPL to log the thoughts from your brain in an organized easy to access structure (SQLite3)

```
_____DO STUFF_____
[2019/02/01 10:35]  |  Starting to do stuff
[2019/02/01 10:36]  |  Doing more stuff
[2019/02/01 10:38]  |  Finished doing all the stuffs

_____DO OTHER STUFF_____
[2019/02/01 10:42]  |  Eesh, this stuff is the worst
[2019/02/01 10:44]  |  Almost done
[2019/02/01 10:51]  |  Never mind it broke
[2019/02/01 10:58]  |  Ah, there! All fixed!
[2019/02/01 10:59]  |  Broke again
[2019/02/01 11:05]  |  Giving up

[2019/02/01 11:08]  |  Taking a nap
[2019/02/01 12:27]  |  woke up hungry

 > \exit
```

---

### Install

To install mindlogger you will need python3 installed on your system. Then simply execute the following command from the root folder of the
project.

```
python setup.py install
```

---

### Run

Once installed, you can run mindlogger from the command line. It takes in an optional parameter (-m --mind) that dictates the name of the
output file in which the logs will be stored. This allows for multiple streams of work and/or multiple users.

```
mindlogger -m {filename}
```

---

### Special Commands

Inside the mindlogger repl there are a few special commands that when executed will trigger events rather than generate logs.

#### Task

This command sets the task on which you are currently working (displayed before the prompt). Any messages typed while 
the task is set will be associated to that task. Leaving the TaskName blank will reset the task to none.

```
\task {TaskName}
```

#### Search

This command allows you to search the current log file by a given date and/or task as well as simply searching for raw text in the messages.
Results will replace the current display of the log file and prompt for user input before resuming normal logging once more.

```
\search -d 2019-01-01 -t MY_TASK RAW SAERCH TEXT
```

#### Exit

This command simply exits the mind logger session. All logs are saved to the file as soon as they are entered, so there is no need
to save anything manually inside mindlogger.

```
\exit
```
