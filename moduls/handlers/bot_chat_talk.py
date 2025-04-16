from aiogram import Router, F
from aiogram.types import Message

import logging

bot_chat_talk_handlers = Router(name=__name__)

bad_fraze = ['/start@test_dev24_bot', '/start@roza_vetrov24_bot']

@bot_chat_talk_handlers.message(F.text.lower() == 'привет')
async def echo_handler(message: Message):
    await message.answer(f'Привет {message.from_user.full_name}, чем я могу помочь?')

@bot_chat_talk_handlers.message(F.text.in_(bad_fraze))
async def del_bad(message: Message):
    await message.delete()

bot_chat_talk_handlers.message.filter(F.chat.type.in_({"group", "supergroup"}))