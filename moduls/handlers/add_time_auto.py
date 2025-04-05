from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from moduls.other.static import main_text, main_photo_path
import logging
from moduls.keyboards.main_keyboard import back_keyboard, user_main_keyboard


add_time_auto_handlers = Router(name=__name__)



@add_time_auto_handlers.callback_query(F.data == 'автомат')
async def select_auto_time(call: CallbackQuery, bot: Bot):
    text = 'Вносим автоматом'

    await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=text),
                                  reply_markup=back_keyboard())

    logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} выбрал указать время старта/финиша')
    await call.answer()


