from aiogram import Router, F
from aiogram.types import Message

import logging

bot_chat_talk_handlers = Router(name=__name__)

@bot_chat_talk_handlers.message(F.text == 'привет')
async def echo_handler(message: Message):
    await message.answer(f'Привет {message.from_user.full_name}, чем я могу помочь?')

