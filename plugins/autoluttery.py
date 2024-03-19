from telethon import TelegramClient, events
import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError
from . import *
@kanha_bot.on(events.NewMessage)
async def lottery(event):
      if 'Welcome to the Poke Lottery.' in event.raw_text:
         await asyncio.sleep(4)
         await event.click(0)
@kanha_bot.on(events.MessageEdited)
async def my_event_handler(event):
      if 'Your numbers:' in event.raw_text:
         await asyncio.sleep(4)
         await event.click(0)
 
@kanh_bot.on(events.MessageEdited)
async def my_event_handler(event):
      if 'Multiplier fee deducted:' in event.raw_text:
         await asyncio.sleep(4)
         await event.click(0)
@kanha_bot.on(events.NewMessage)
async def my_event_handler(event):
      if 'Your numbers:' in event.raw_text:
         await asyncio.sleep(4)
         await event.click(0, 0)
         await event.click(text='Random')
