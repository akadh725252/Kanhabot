# made by @moiuname < dot arc >

import asyncio
from random import choice, randrange
from re import search
import os
import sys

from telethon.events import NewMessage, MessageEdited
from telethon.errors import DataInvalidError, MessageNotModifiedError
from telethon.tl.custom import Message

from . import *


HEXA_ID = 572621020


async def get_response(
    chat,
    user_id,
    message,
    func=None,
    **kwargs,
):
    timeout = kwargs.pop("timeout", 60)
    reply_to = kwargs.pop("reply_to", None)
    async with kanha_bot.conversation(chat, timeout=timeout) as conv:
        response = conv.wait_event(
            NewMessage(
                incoming=True,
                from_users=user_id,
                func=func,
                **kwargs,
            )
        )
        await conv.send_message(message, reply_to=reply_to)
        response = await response
        return response


async def re_fetch(m):
    return await m.client.get_messages(m.chat_id, ids=m.id)


async def watch_edits(chat, msg_id, timeout=16):
    async with kanha_bot.conversation(chat, timeout=timeout) as conv:
        func = lambda e: e.id == msg_id and search(
            rf"(?i)Current turn: (.+){kanha_bot.uid}", e.message.text
        )
        response = conv.wait_event(
            MessageEdited(
                incoming=True,
                from_users=HEXA_ID,
                func=func,
            )
        )
        response = await response
        await asyncio.sleep(3)
        response = await re_fetch(response)
        return response


async def do_click(msg, *buttons):
    async def _click():
        try:
            await msg.click(*buttons)
        except DataInvalidError:
            pass

    async def _loop():
        nonlocal msg
        for _ in range(3):
            await asyncio.sleep(2)
            r_msg = await re_fetch(msg)
            if r_msg and r_msg.buttons and r_msg.text == msg.text:
                await _click()
                msg = r_msg
            else:
                return

    await _click()
    asyncio.create_task(_loop())


async def main(e, other_usr):
    try:
        usr_response = await get_response(
            chat=e.chat_id,
            user_id=other_usr,
            message="/fakeChallenge",
            pattern=r"^\#ReadyforBattle$",
        )
    except asyncio.TimeoutError:
        raise TypeError("No response from 2nd ID")

    try:
        await asyncio.sleep(1)
        hexa_response = await get_response(
            chat=e.chat_id,
            user_id=HEXA_ID,
            message="/challenge",
            timeout=20,
            reply_to=usr_response.id,
        )
    except asyncio.TimeoutError:
        raise TypeError("No response from Hexa Bot!")

    try:
        await e.edit(
            f"**Challenge Sent.** \n\nWaiting to get accept!"
        )
        await asyncio.sleep(1)
    except MessageNotModifiedError:
        pass

    while True:
        response = await watch_edits(e.chat_id, hexa_response.id)
        if isinstance(response, Message):
            resp = await do_click(response, 0, 0)
            if resp == True:
                return
async def watch_newmessage(chat, msg_id, timeout=6):
    async with kanha_bot.conversation(chat, timeout=timeout) as conv:
        func2 = "Daily limit for battling has been reached, no prize will be given"
        response = conv.wait_event(
            MessageEdited(
                incoming=True,
                from_users=HEXA_ID,
            )
        )
    while True:
        response = await watch_newmessage(e.chat_id,hexa_response.id)
        if func2 in response.raw_text:
            os.execl(sys.executable, sys.executable, *sys.argv)
@kanha_cmd(
    pattern="hexa( (.*)|$)",
)
async def autohexa(e):
    i = True
    await e.respond("team changing")
    if i == True:
      chat = e.chat_id
      async with kanha_bot.conversation(chat) as conv :
        await conv.send_message("/myteam")
        resp = await conv.get_response(timeout=16)
        await asyncio.sleep(2)
        await resp.click(text="Team 1")
        await asyncio.sleep(2)
        await resp.click(text="Team 1")
        await asyncio.sleep(2)
        await resp.click(text="Team 1")
        await asyncio.sleep(2)
        await conv.send_message('done.click.team1')
        await asyncio.sleep(30)
    args = e.pattern_match.group(2)
    if not args:
        return await e.eor("`Whom should I fight with..?`", time=8)

    try:
        count, other_usr = args.split(" ", maxsplit=1)
    except Exception:
        return await e.eor("Use .hexa 5 123456789")

    try:
        count = int(count)
        if count < 0:
            raise ValueError
        count += 1
    except ValueError:
        return await e.eor("`Invalid Count..` ðŸ¤¡", time=5)

    try:
        other_usr = int(other_usr)
        if other_usr < 0:
            raise ValueError
    except ValueError:
        return await e.eor("`Invalid user..` ðŸ¤¡", time=5)

    domt = await e.eor(f"**Auto Battle Running for {count} times!..**")
    success = 0
    for _ in range(1, count):
        try:
            await main(domt, other_usr)
        except asyncio.TimeoutError:
            await domt.reply(f"Got Timeout Error.. Stopping run #{_}")
            continue
        except Exception as exc:
            LOGS.exception(exc)
            await domt.reply(f"**Got {exc.__class__} in run #{_}** \n\n`{exc}`")
            continue
        else:
            success += 1
            await domt.edit(f"__Finished run #{_}__")
        finally:
            # sleep between runs
            await asyncio.sleep(6)

    await domt.edit(f"**Finished AutoHexa!\n\nFailed #{count - success} times!**")
