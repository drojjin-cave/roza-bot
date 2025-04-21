import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Router, html, F, Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.filters import CommandStart, Command
import logging
from moduls.other.static import main_text, main_photo_path, send_protocol_text
from moduls.keyboards.main_keyboard import *
from aiogram.fsm.context import FSMContext

from moduls.settings import settings
from moduls.utils.states_form import SendProtocol
from moduls.handlers.basic import mes_start, google_sheet_base


send_protokol_handlers = Router(name=__name__)

ADMIN_CHANNEL = settings.bots.admin_channel
ADMIN_TEST = '504535913'


@send_protokol_handlers.message(Command("send_protocol"))
async def get_help(message: Message, bot: Bot, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        try:
            await message.delete()
            await bot.edit_message_reply_markup(message_id=mes_start[0].message_id, reply_markup=None, chat_id=message.chat.id)
            await message.answer(send_protocol_text)

            #await bot.edit_message_caption(message_id=mes_start.message_id, reply_markup=None, chat_id=message.chat.id, caption=help_text)
            await state.set_state(SendProtocol.SEND_PROTOCOL)
        except:
            await message.answer('Были обнаружены доработки, пожалуйста, перезапустите бота')
    else:
        await message.delete()
        mes_error_protocol = await message.answer('Раздел отправки протокола работает только из главного меню\nзавершите ввод данных!')
        await asyncio.sleep(3)
        await bot.delete_message(chat_id=message.chat.id, message_id=mes_error_protocol.message_id)


        #await bot.edit_message_reply_markup(message_id=mes_start.message_id, reply_markup=None, chat_id=message.chat.id)



@send_protokol_handlers.message(SendProtocol.SEND_PROTOCOL)
async def help_answer(message: Message, state: FSMContext, bot: Bot):

    db_bot = google_sheet_base.read_data('Пользователи!A2:G')
    name_referee = None
    try:
        for row in db_bot:
            if str(message.from_user.id) == row[0]:
                name_referee = row[6]
                break
    except:
        name_referee = message.from_user.full_name

    date_update_info = datetime.now(timezone.utc)
    date_update_info = (date_update_info + timedelta(hours=7, minutes=0)).strftime('%d.%m.%Y %H:%M:%S')

    text = (f'Получен протокол от <b>@{message.from_user.username}</b>\n\n'
            f'<blockquote>Время - <b>{date_update_info}</b>\n'
            f'Судья - <b>{name_referee}</b></blockquote>'
            )

    if message.caption:
        await bot.send_photo(chat_id=ADMIN_CHANNEL, photo=message.photo[-1].file_id,
                         caption=text + f'\n\n<b>Сообщение от судьи:</b>\n<blockquote>{message.caption}</blockquote>')
        text_answer = ('\nПротокол отправлен орг. комитету!\n'
                       'Ты просто космос!👽\n\n'
                       'Через несколько секунд появится главное меню...')
        await message.reply(text_answer)
        logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} отправил протокол')

    else:
        if message.photo:
            await bot.send_photo(chat_id=ADMIN_CHANNEL, photo=message.photo[-1].file_id, caption=text)
            logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} отправил протокол')

            text_answer = ('\nПротокол отправлен орг. комитету!\n'
                           'Ты просто космос!👽\n\n'
                           'Через несколько секунд появится главное меню...')
            await message.reply(text_answer)
        else:
            await message.answer('<b>Похоже вы не прикрепили фото протокола, попробуйте снова</b>!\n\nЧерез несколько секунд появится главное меню...')


    await state.clear()

    await asyncio.sleep(5)
    global mes_start
    mes_start[0] = await bot.send_photo(message.from_user.id, photo=FSInputFile(path=main_photo_path), caption=main_text,
                                     reply_markup=user_main_keyboard())



