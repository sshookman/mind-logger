from pathlib import Path

import os
import yaml

from .styles import codes

class config():
    reset = "\033[0m"
    activeTaskColor = None
    dateHeaderColor = None

    def __init__(self):
        cfgFile = "{home}/mindlogger.yaml".format(home=str(Path.home()))

        cfg = None
        if os.path.isfile(cfgFile):
            with open(cfgFile, 'r') as stream:
                cfg = yaml.load(stream)

        self.activeTaskColor = parseStyle(cfg, "active-task", "\033[0m\033[36m\033[1m")
        self.dateHeaderColor = parseStyle(cfg, "date-header", "\033[0m\033[44m\033[1m")

    def parseStyle(config, name, default):
        style = default
        if (config):
            if ("style" in config):
                if (name in config["style"]):
                    style = ""
                    for styleName in config["style"].get(name, ""):
                        style += codes.get(styleName, "")

        return style

    def getActiveTaskColor(self):
        return self.activeTaskColor

    def getDateHeaderColor(self):
        return self.dateHeaderColor
