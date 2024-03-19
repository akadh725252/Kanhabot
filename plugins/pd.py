import asyncio
from telethon import TelegramClient, events
import re
from telethon.tl.functions.channels import GetFullChannelRequest
from . import *
@kanha_cmd(pattern='pd')
async def pd(e):
 chat = -1001737654150
 pinchat = -1001737654150
 a = await e.client(GetFullChannelRequest(pinchat))
 pinmsg = a.full_chat.pinned_msg_id
 async with e.client.conversation(chat) as conv:
  await conv.send_message('/myinventory')
  try:
   a = await conv.get_response(timeout=8)
   if 'Poke Dollars' in a.text:
    amount = re.search(r'💵: (\d+)', a.text)
    if amount:
     amount = int(amount.group(1))
     await asyncio.sleep(3)
     await e.client.send_message(pinchat, f'/give {amount}', reply_to=pinmsg)
  except asyncio.TimeoutError:
   await e.edit('Bot not responding')