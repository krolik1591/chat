async def create_ref_link(state, user_id):
    bot_username = (await state.bot.me()).username
    text = f'http://t.me/{bot_username}?start={user_id}'
    return text
