# kanha - UserBot
# Copyright (C) 2021-2023 Teamkanha
#
# This file is a part of < https://github.com/Teamkanha/kanha/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Teamkanha/kanha/blob/main/LICENSE/>.

from . import get_help

__doc__ = get_help("help_bot")

import os
import sys
import time
import asyncio
from random import randrange
from re import search

from telethon.events import NewMessage, MessageEdited
from telethon.errors import DataInvalidError

from . import *
from platform import python_version as pyver
from random import choice

from telethon import __version__
from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    ChatSendMediaForbiddenError,
)

from pykanha.version import __version__ as UltVer

from . import HOSTED_ON, LOGS

try:
    from git import Repo
except ImportError:
    LOGS.error("bot: 'gitpython' module not found!")
    Repo = None

from telethon.utils import resolve_bot_file_id

from . import (
    ATRA_COL,
    LOGS,
    OWNER_NAME,
    ULTROID_IMAGES,
    Button,
    Carbon,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    inline_pic,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    kanha_cmd,
    kanha_version,
    updater,
)


def ULTPIC():
    return inline_pic() or choice(ULTROID_IMAGES)


buttons = [
    [
        Button.url(get_string("bot_3"), "https://github.com/Teamkanha/kanha"),
        Button.url(get_string("bot_4"), "t.me/kanhaSupportChat"),
    ]
]

# Will move to strings
alive_txt = """
The kanha Userbot

  ◍ Version - {}
  ◍ Py-kanha - {}
  ◍ Telethon - {}
"""

in_alive = "{}\n\n🌀 <b>kanha Version -><b> <code>{}</code>\n🌀 <b>Pykanha -></b> <code>{}</code>\n🌀 <b>Python -></b> <code>{}</code>\n🌀 <b>Uptime -></b> <code>{}</code>\n🌀 <b>Branch -></b>[ {} ]\n\n• <b>Join @Teamkanha</b>"


@callback("alive")
async def alive(event):
    text = alive_txt.format(kanha_version, UltVer, __version__)
    await event.answer(text, alert=True)


@kanha_cmd(
    pattern="alive( (.*)|$)",
)
async def lol(ult):
    match = ult.pattern_match.group(1).strip()
    inline = None
    if match in ["inline", "i"]:
        try:
            res = await ult.client.inline_query(asst.me.username, "alive")
            return await res[0].click(ult.chat_id)
        except BotMethodInvalidError:
            pass
        except BaseException as er:
            LOGS.exception(er)
        inline = True
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = "main"
    xx = "kanha"
    rep = "@kanha_garg1"
    kk = f" `[{y}]({rep})` "
    if inline:
        kk = f"<a href={rep}>{y}</a>"
        parse = "html"
        als = in_alive.format(
            header,
            f"{kanha_version} [{HOSTED_ON}]",
            UltVer,
            pyver(),
            uptime,
            kk,
        )

        if _e := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("🌀", _e)
    else:
        parse = "md"
        als = (get_string("alive_1")).format(
            header,
            OWNER_NAME,
            f"{kanha_version} [{HOSTED_ON}]",
            UltVer,
            uptime,
            pyver(),
            __version__,
            kk,
        )

        if a := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("✵", a)
    if pic:
        try:
            await ult.reply(
                als,
                file=pic,
                parse_mode=parse,
                link_preview=False,
                buttons=buttons if inline else None,
            )
            return await ult.try_delete()
        except ChatSendMediaForbiddenError:
            pass
        except BaseException as er:
            LOGS.exception(er)
            try:
                await ult.reply(file=pic)
                await ult.reply(
                    als,
                    parse_mode=parse,
                    buttons=buttons if inline else None,
                    link_preview=False,
                )
                return await ult.try_delete()
            except BaseException as er:
                LOGS.exception(er)
    await eor(
        ult,
        als,
        parse_mode=parse,
        link_preview=False,
        buttons=buttons if inline else None,
    )


@kanha_cmd(pattern="ping$", chats=[], type=["official", "assistant"])
async def _(event):
    start = time.time()
    x = await event.eor("Pong !")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(get_string("ping").format(end, uptime))


@kanha_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API


@kanha_cmd(
    pattern="restart$",
    fullsudo=True,
)
async def restartbt(ult):
    ok = await ult.eor(get_string("bot_5"))
    call_back()
    who = "bot" if ult.client._bot else "user"
    udB.set_key("_RESTART", f"{who}_{ult.chat_id}_{ok.id}")
    if heroku_api:
        return await restart(ok)
    await bash("git pull && pip3 install -r requirements.txt")
    if len(sys.argv) > 1:
        os.execl(sys.executable, sys.executable, "main.py")
    else:
        os.execl(sys.executable, sys.executable, "-m", "pykanha")


@kanha_cmd(
    pattern="shutdown$",
    fullsudo=True,
)
async def shutdownbot(ult):
    await shutdown(ult)


@kanha_cmd(
    pattern="logs( (.*)|$)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1).strip()
    file = f"kanha{sys.argv[-1]}.log" if len(sys.argv) > 1 else "kanha.log"
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.eor(get_string("com_1"))
        with open(file, "r") as f:
            code = f.read()[-2500:]
        file = await Carbon(
            file_name="kanha-logs",
            code=code,
            backgroundColor=choice(ATRA_COL),
        )
        if isinstance(file, dict):
            await event.eor(f"`{file}`")
            return
        await event.reply("**kanha Logs.**", file=file)
    elif opt == "open":
        with open("kanha.log", "r") as f:
            file = f.read()[-4000:]
        return await event.eor(f"`{file}`")
    else:
        await def_logs(event, file)
    await event.try_delete()


@in_pattern("alive", owner=True)
async def inline_alive(ult):
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f"<a href={rep}>{y}</a>"
    als = in_alive.format(
        header, f"{kanha_version} [{HOSTED_ON}]", UltVer, pyver(), uptime, kk
    )

    if _e := udB.get_key("ALIVE_EMOJI"):
        als = als.replace("🌀", _e)
    builder = ult.builder
    if pic:
        try:
            if ".jpg" in pic:
                results = [
                    await builder.photo(
                        pic, text=als, parse_mode="html", buttons=buttons
                    )
                ]
            else:
                if _pic := resolve_bot_file_id(pic):
                    pic = _pic
                    buttons.insert(
                        0, [Button.inline(get_string("bot_2"), data="alive")]
                    )
                results = [
                    await builder.document(
                        pic,
                        title="Inline Alive",
                        description="@Teamkanha",
                        parse_mode="html",
                        buttons=buttons,
                    )
                ]
            return await ult.answer(results)
        except BaseException as er:
            LOGS.exception(er)
    result = [
        await builder.article(
            "Alive", text=als, parse_mode="html", link_preview=False, buttons=buttons
        )
    ]
    await ult.answer(result)


@kanha_cmd(pattern="update( (.*)|$)")
async def _(e):
    xx = await e.eor(get_string("upd_1"))
    if e.pattern_match.group(1).strip() and (
        "fast" in e.pattern_match.group(1).strip()
        or "soft" in e.pattern_match.group(1).strip()
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "pykanha")
        # return
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            udB.get_key("LOG_CHANNEL"),
            ULTPIC(),
            caption="• **Update Available** •",
            force_document=False,
            buttons=Button.inline("Changelogs", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/Teamkanha/kanha/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        ULTPIC(),
        caption="• **Update Available** •",
        force_document=False,
        buttons=Button.inline("Changelogs", data="changes"),
    )

HEXA_ID = 572621020


async def re_fetch(m):
    return await m.client.get_messages(m.chat_id, ids=m.id)


async def watch_edits(chat, msg_id, timeout=20):
    async with kanha_bot.conversation(chat, timeout=timeout) as conv:
        func = lambda e: e.id == msg_id and search(rf"(?i)Current turn: (.+){kanha_bot.uid}", e.message.text)
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


# try clicking button 3 times in background. (2s delay)
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


# clicks ready button
async def get_ready(chat):
    async with kanha_bot.conversation(chat, timeout=16) as conv:
        response = conv.wait_event(
            NewMessage(incoming=True, from_users=HEXA_ID, func=lambda e: e.mentioned)
        )
        response = await response
        if response.buttons and response.buttons[0][0].text.startswith("Ready"):
            await asyncio.sleep(3)
            await do_click(response, 0, 0)
            await asyncio.sleep(3)
            return response.id


# clicks button b/w (2-6)
async def click_rnd_button(msg):
    for count1, sub_buttons in enumerate(msg.buttons):
        for count2, button in enumerate(sub_buttons):
            text = str(button.text).strip()
            if text and text.isdigit():
                return await do_click(msg, count1, count2)


# click (attack) if dodged or missed otherwise pokemon -> 2 to 6
async def auto_battle(chat, msg_id):
    response = await watch_edits(chat, msg_id, timeout=15)
    await asyncio.sleep(2)
    if not response.buttons:
        return True
    elif "team" in response.buttons[0][0].text.lower():
        return await click_rnd_button(response)
    else:
        rndm = lambda: randrange(2)
        return await do_click(response, rndm(), rndm())

@kanha_bot.on(
    NewMessage(
        incoming=True,
        pattern="^/fakeChallenge$",
        from_users=udB.get_key("SUDOS"),
    )
)
async def autohemxa(e):
    await asyncio.sleep(1)
    msg = await e.reply("#ReadyforBattle")
    try:
        hexa_msg_id = await get_ready(e.chat_id)
        await msg.delete()
        while True:
            response = await auto_battle(e.chat_id, hexa_msg_id)
            # await asyncio.sleep(0.3)
            if response == True:
                return
    except asyncio.TimeoutError:
        return await msg.respond("Timeout Error.. Skipping!")
    except Exception as exc:
        LOGS.exception(exc)
        await msg.respond(f"**2nd ID Error** \n\nGot {exc.__class__} \n`{exc}`")

@kanha_bot.on(events.NewMessage( incoming=True))
async def x(event) :
  chat = "HeXamonbot"
  if "done.click.team1" in event.raw_text :
    async with kanha_bot.conversation(chat) as conv :
      await conv.send_message("/myteam")
      await asyncio.sleep(2)
      a = await conv.get_response()
      if a :
        await a.click(text = 'Team 2')
      if not a :
        await conv.send_message("/myteam")
      await event.respond(a)
      await asyncio.sleep(2)
      b = await conv.get_response()
      if b :
        await b.click(text = 'Team 2')
