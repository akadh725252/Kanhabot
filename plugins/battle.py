from telethon import events, TelegramClient
from asyncio import sleep as zzz
from random import randint
import os
import sys

from . import *

chat = 572621020
hunt = False
list = ["A wild"]

@kanha_bot.on(events.NewMessage(outgoing=True, pattern='.bgo'))
async def begin(event):
    global hunt
    hunt = True
    await event.edit('going for hexa battles')
    x = await kanha_bot.send_message(chat, "/hunt")
    try:
        async with kanha_bot.conversation('@Hexamonbot') as conv:
            await conv.get_response(x.id)
    except:
        await zzz(1, 3)
        await kanha_bot.send_message(chat, "/hunt")

@kanha_bot.on(events.NewMessage(chats=chat, incoming=True))
async def handle_hunt(event):
    global hunt
    if hunt:
        text = event.message.text
        hun = True
        message = await kanha_bot.get_messages(chat, ids=event.message.id)
        if "✨" in event.raw_text:
            await zzz(randint(1, 2))
            await message.click(text='Poke Balls')
            await message.click(text='Ultra')
            await message.click(text='Great')
            pass
        elif "TM" in event.raw_text:
            print(event.message.text)
            await zzz(randint(5, 7))
            x = await kanha_bot.send_message(chat, "/hunt")
            try:
                async with kanha_bot.conversation('@Hexamonbot') as conv:
                    await conv.get_response(x.id)
            except:
                await zzz(3, 7)
                await kanha_bot.send_message(chat, "/hunt")
        elif any(item in text for item in list) and hunt:
            await message.click(0)
            await message.click(0, 1)
            await message.click(text="Battle")
        elif "An expert" in text and hunt:
            if not hun:
                pass
            else:
                await zzz(randint(6, 8))
                x = await kanha_bot.send_message(chat, "/hunt")
                try:
                    async with kanha_bot.conversation('@Hexamonbot') as conv:
                        await conv.get_response(x.id)
                except:
                    await zzz(3, 5)
                    await kanha_bot.send_message(chat, "/hunt")
        elif "Daily limit for battling" in event.raw_text:  
          hunt=False
@kanha_bot.on(events.MessageEdited(chats=chat))
async def cacther(event):
    if hunt:
        message = await kanha_bot.get_messages(chat, ids=event.message.id)
        await message.click(1, 1)
        await message.click(0, 0)
        await message.click(1, 0)
        
        if any(keyword in event.message.text for keyword in ['fled', 'fainted', 'caught', '+']):
            await zzz(randint(2, 5))
            x = await kanha_bot.send_message(chat, "/hunt")
            try:
                async with kanha_bot.conversation('@Hexamonbot') as conv:
                    await conv.get_response(x.id)
            except:
                await zzz(1, 3)
                await kanha_bot.send_message(chat, "/hunt")

@kanha_bot.on(events.NewMessage(outgoing=True, pattern='.bstop'))
async def stop(event):
    global hunt
    hunt = False

@kanha_bot.on(events.NewMessage(chats=chat, incoming=True))
async def handle_battle(event):
    if hunt:
        print(event.message.text)
        if event.message.text[:13] == "Battle begins":
            message = await kanha_bot.get_messages(chat, ids=event.message.id)
            await zzz(2)
            await message.click(0, 1)
            await message.click(0, 0)
            await message.click(1, 0)
