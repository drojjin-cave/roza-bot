from datetime import datetime, timezone, timedelta

from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

import logging

from moduls.settings import settings
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
from moduls.other.static import token_sheet

bot_chat_talk_handlers = Router(name=__name__)
ADMIN_CHANNEL = settings.bots.admin_channel

bad_fraze = ['/start@test_dev24_bot', '/start@roza_vetrov24_bot', '/help@test_dev24_bot', '/help@roza_vetrov24_bot', '/send_protocol@roza_vetrov24_bot']

id_table = '1zYjSJhbwD_lwWMIYx4h7uJC6YIuWkzlmDzDhWBP1dX4'
google_sheet = GoogleSheet(token_sheet, id_table)

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


@bot_chat_talk_handlers.message(F.text.lower().startswith('инфо'))
async def send_info(message: Message):
    mes = message.text
    mes = mes.split()
    try:
        mes = [mes[1].capitalize(), mes[2].capitalize()]
        mes = ' '.join(mes)

        range_name = 'Данные участников сводка'
        info = google_sheet.info(range_name, mes)

        text_send = (f'Краткая сводка <b>{mes}:</b>\n\n'
                     f'<blockquote>Общее колчество участников - <b>{info["Колчество участников"]}</b>\n'
                     f'Прошли дистанцию - <b>{info["Пройдено дистанцию"]}</b>\n'
                     f'Лучшее время - <b>{info["Лучшее время"]}</b>\n'
                     f'Худшее время - <b>{info["Худшее время"]}</b>\n'
                     f'Превысили КВ - <b>{info["Превышено КВ"]}</b></blockquote>')


        await message.answer(text_send)
    except:
        await message.answer('Не верный запрос')

bot_chat_talk_handlers.message.filter(F.chat.type.in_({"group", "supergroup"}))