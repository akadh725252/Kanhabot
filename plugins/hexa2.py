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
