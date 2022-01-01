# Discord Imports
import discord

# Other Imports
from enum import Enum, auto
from datetime import datetime
import os


class StatusType(Enum):
    ERROR = auto()
    WARNING = auto()
    OK = auto()


class Logger:
    def __init__(self, bot: discord.ext.commands.Bot, log_file_path: str):
        self._bot = bot
        self.file_dir = log_file_path

    def write(self, *, status: StatusType, message: str):
        new_log_line = f"""[{datetime.now()}]
[Status: {status}]
{message}
===================================================================================\n"""
        print(new_log_line)
        with open(f"{self.file_dir}", "a") as f:
            f.write(new_log_line)
