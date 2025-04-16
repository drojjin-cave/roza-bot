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
from moduls.handlers.basic import mes_start


send_protokol_handlers = Router(name=__name__)

ADMIN_CHANNEL = settings.bots.admin_channel


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


    date_update_info = datetime.now(timezone.utc)
    date_update_info = (date_update_info + timedelta(hours=7, minutes=0)).strftime('%d.%m.%Y %H:%M:%S')

    text = (f'Получен протокол от <b>@{message.from_user.username}</b>\n\n'
            f'<blockquote>Время - <b>{date_update_info}</b>\n'
            f'Судья - <b>{message.from_user.full_name}</b></blockquote>'
            )


    await bot.send_photo(chat_id=ADMIN_CHANNEL, photo=message.photo[-1].file_id,
                         caption=text)

    text_answer = ('\nПротокол отправлен орг. комитету!\n'
                    'Ты просто космос!👽\n\n'
                   'Через несколько секунд появится главное меню...')
    await message.reply(text_answer)
    await state.clear()

    await asyncio.sleep(5)
    global mes_start
    mes_start[0] = await bot.send_photo(message.from_user.id, photo=FSInputFile(path=main_photo_path), caption=main_text,
                                     reply_markup=user_main_keyboard())



