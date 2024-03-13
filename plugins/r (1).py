import os
import sys
import time
import asyncio
from random import randrange
from re import search
from telethon.tl.functions.messages import EditMessageRequest
from telethon.tl.custom import Message
from telethon import TelegramClient
from telethon import events
from . import *

@kanha_cmd(pattern="r$", fullsudo=True,)
async def restart(event):
    await event.edit("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)
