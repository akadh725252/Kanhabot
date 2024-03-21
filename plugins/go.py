from telethon import events, TelegramClient
from asyncio import sleep as zzz
from random import randint

chat = 572621020
hunt = False
pokeballs = ["Poke Balls"]

@kanha_bot.on(events.NewMessage(outgoing=True, pattern='.go'))
async def begin(event):
    global hunt
    hunt = True
    await event.edit('going for hexa battles')
    x = await kanha_bot.send_message(chat, "/hunt")
    try:
        async with kanha_bot.conversation('@Hexamonbot') as conv:
            await conv.get_response(x.id)
    except Exception as e:
        print(f"Error in beginning hunt: {str(e)}")
        await zzz(1, 3)
        await kanha_bot.send_message(chat, "/hunt")

@kanha_bot.on(events.NewMessage(chats=chat, incoming=True))
async def handle_hunt(event):
    global hunt
    if hunt and event.message:
        text = event.message.text
        try:
            message = await kanha_bot.get_messages(chat, ids=event.message.id)
            if "✨" in text:
                if message.buttons:
                    await message.click(text='Poke Balls')
                    await zzz(randint(5, 7))
                    await message.click(text='Ultra')
                    await message.click(text='Great')
            elif "TM" in text:
                print(event.message.text)
                if message.buttons:
                    await zzz(randint(5, 7))
                    x = await kanha_bot.send_message(chat, "/hunt")
                    try:
                        async with kanha_bot.conversation('@Hexamonbot') as conv:
                            await conv.get_response(x.id)
                    except Exception as e:
                        print(f"Error in handling TM: {str(e)}")
                        await zzz(3, 7)
                        await kanha_bot.send_message(chat, "/hunt")
            elif any(item in text for item in pokeballs):
                if message.buttons:
                    await message.click(0)
                    await message.click(0, 1)
                    await message.click(text="Battle")
            elif expert in text:
                if not hun:
                    pass
                else:
                    if message.buttons:
                        await zzz(randint(6, 8))
                        x = await kanha_bot.send_message(chat, "/hunt")
                        try:
                            async with kanha_bot.conversation('@Hexamonbot') as conv:
                                await conv.get_response(x.id)
                        except:
                            await zzz(3, 5)
                            await kanha_bot.send_message(chat, "/hunt")
            elif "Daily limit for battling" in text:
                hunt = False
        except Exception as e:
            print(f"Error in handling hunt: {str(e)}")

@kanha_bot.on(events.MessageEdited(chats=chat))
async def cacther(event):
    if hunt and event.message:
        try:
            message = await kanha_bot.get_messages(chat, ids=event.message.id)
            if message.buttons:
                await message.click(1, 1)
                
                if any(keyword in event.message.text for keyword in ['fled', 'fainted', 'caught', '+']):
                    await zzz(randint(2, 5))
                    x = await kanha_bot.send_message(chat, "/hunt")
                    try:
                        async with kanha_bot.conversation('@Hexamonbot') as conv:
                            await conv.get_response(x.id)
                    except Exception as e:
                        print(f"Error in catching the message: {str(e)}")
                        await zzz(1, 3)
                        await kanha_bot.send_message(chat, "/hunt")
        except Exception as e:
            print(f"Error in handling message edit: {str(e)}")

@kanha_bot.on(events.NewMessage(outgoing=True, pattern='.bstop'))
async def stop(event):
    global hunt
    hunt = False

@kanha_bot.on(events.NewMessage(chats=chat, incoming=True))
async def handle_battle(event):
    if hunt and event.message:
        print(event.message.text)
        if event.message.text[:13] == "Battle begins" and event.message.buttons:
            message = await kanha_bot.get_messages(chat, ids=event.message.id)
            await zzz(2)
            await message.click(0, 1)
