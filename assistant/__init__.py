# kanha - UserBot
# Copyright (C) 2021-2023 Teamkanha
#
# This file is a part of < https://github.com/Teamkanha/kanha/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Teamkanha/kanha/blob/main/LICENSE/>.

from telethon import Button, custom

from plugins import ATRA_COL, InlinePlugin
from pykanha import *
from pykanha import _ult_cache
from pykanha._misc import owner_and_sudos
from pykanha._misc._assistant import asst_cmd, callback, in_pattern
from pykanha.fns.helper import *
from pykanha.fns.tools import get_stored_file
from strings import get_languages, get_string

OWNER_NAME = kanha_bot.full_name
OWNER_ID = kanha_bot.uid

AST_PLUGINS = {}


async def setit(event, name, value):
    try:
        udB.set_key(name, value)
    except BaseException as er:
        LOGS.exception(er)
        return await event.edit("`Something Went Wrong`")


def get_back_button(name):
    return [Button.inline("« Bᴀᴄᴋ", data=f"{name}")]
