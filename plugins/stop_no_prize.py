from telethon import TelegramClient, events
import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError
from . import *
@kanha_bot.on(events.MessageEdited)
async def my_event_handler(event):
      if 'Daily limit for battling has been reached, no prize will be given' in event.raw_text:
               await restart(event)