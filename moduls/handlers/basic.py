from aiogram import Router, html, F, Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.filters import CommandStart, Command
import logging
from moduls.other.static import main_text, main_photo_path
from moduls.keyboards.main_keyboard import *
from aiogram.fsm.context import FSMContext

from moduls.utils.comands import set_commands

basic_handlers = Router(name=__name__)


@basic_handlers.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot, state: FSMContext):
    await set_commands(bot)
    await state.clear()
    await bot.send_photo(message.from_user.id, photo=FSInputFile(path=main_photo_path), caption=main_text, reply_markup=user_main_keyboard())

    logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} нажал кнопку старт')


@basic_handlers.callback_query(F.data == 'назад')
async def back(call: CallbackQuery, bot: Bot):
    await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=main_text),
                                  reply_markup=user_main_keyboard())

    await call.answer()

basic_handlers.message.filter(F.chat.type == "private")