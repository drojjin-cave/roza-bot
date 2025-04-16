from aiogram import Router, html, F, Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.filters import CommandStart, Command
import logging
from moduls.other.static import main_text, main_photo_path
from moduls.keyboards.main_keyboard import *
from aiogram.fsm.context import FSMContext

from moduls.utils.comands import set_commands
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
from moduls.other.static import token_sheet

id_table = '1LjYgO3xAXoi1kC828beed1hBMTuDmOCt4iQvAUBqC84'  # База данных бота
google_sheet_base = GoogleSheet(token_sheet, id_table)

basic_handlers = Router(name=__name__)


@basic_handlers.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot, state: FSMContext):
    await set_commands(bot)
    await state.clear()
    await bot.send_photo(message.from_user.id, photo=FSInputFile(path=main_photo_path), caption=main_text, reply_markup=user_main_keyboard())

    logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} нажал кнопку старт')

    id_users = google_sheet_base.read_data('Пользователи!A2:A')
    if str(message.from_user.id) not in id_users:

        data = [[message.from_user.id,
                 message.from_user.first_name,
                 message.from_user.last_name,
                 message.from_user.username]]


        google_sheet_base.write_data('Пользователи!A2:D', data)
        logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} занесен в базу данных')



@basic_handlers.callback_query(F.data == 'назад')
async def back(call: CallbackQuery, bot: Bot):
    await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=main_text),
                                  reply_markup=user_main_keyboard())

    await call.answer()

basic_handlers.message.filter(F.chat.type == "private")