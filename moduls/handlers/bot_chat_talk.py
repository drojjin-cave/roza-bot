from datetime import datetime, timezone, timedelta

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

import logging

from moduls.settings import settings

bot_chat_talk_handlers = Router(name=__name__)
ADMIN_CHANNEL = settings.bots.admin_channel

bad_fraze = ['/start@test_dev24_bot', '/start@roza_vetrov24_bot', '/help@test_dev24_bot', '/help@roza_vetrov24_bot']

@bot_chat_talk_handlers.message(F.text.lower() == 'привет')
async def echo_handler(message: Message):
    await message.answer(f'Привет {message.from_user.full_name}, чем я могу помочь?')

@bot_chat_talk_handlers.message(F.text.in_(bad_fraze))
async def del_bad(message: Message):
    await message.delete()


@bot_chat_talk_handlers.message(F.text.lower().startswith('логи'))
async def send_logs(message: Message, bot: Bot, n=30):

    if message.text.isalpha():
        n = int("-" + str(n))
    elif not message.text.isalpha():
        n = int("-" + message.text.split()[1])
    log = r'/home/drojjin/.pm2/logs/tg-roza-error.log'

    date_update_info = datetime.now(timezone.utc)
    date_update_info = (date_update_info + timedelta(hours=7, minutes=0)).strftime('%d.%m.%Y %H:%M:%S')

    log_out = f'/home/drojjin/projects/logs/roza/logs-roza-send.log'

    with open(log, mode="r") as logs:
        logs = logs.readlines()
    with open(log_out, mode='w') as logs_out:
        logs_out.write("".join(logs[-1:n:-1]))

    text = (f'Последние {str(n)[1:]} строк логов\n'
            f'Время - <b>{date_update_info}</b>')

    await bot.send_document(ADMIN_CHANNEL, document=FSInputFile(path=log_out), caption=text)

bot_chat_talk_handlers.message.filter(F.chat.type.in_({"group", "supergroup"}))