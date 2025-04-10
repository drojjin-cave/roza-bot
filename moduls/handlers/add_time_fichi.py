from aiogram import Bot, Router, F
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from aiogram.types import CallbackQuery
from aiogram.filters import Command
import asyncio

from moduls.keyboards.main_keyboard import user_main_keyboard
from moduls.other.static import token_sheet, main_photo_path, main_text
from moduls.keyboards.time_key import stop_view
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
from moduls.utils.additional import print_table


add_time_fichi_handlers = Router(name=__name__)
google_sheet_fichi = GoogleSheet(token_sheet)

@add_time_fichi_handlers.callback_query(F.data == 'просмотр')
async def get_added_users(call: CallbackQuery, bot: Bot):

    all_data = google_sheet_fichi.read_data('Данные')
    data_referee = google_sheet_fichi.search_referee(call.from_user.id, all_data)
    if data_referee:
        head = ['<b>ID</b>','<b>Время</b>', '<b>Имя</b>']
        width_head = 7

        data = []
        for user in data_referee:
            data.append([user["ID"], user["Время"], user["Имя"]])

        data_format = print_table(data, 6)
        data_format.insert(0, f'{" " * width_head}'.join(head))
        data = '\n'.join(data_format)
        text_to_send = f"<b>Введенные вами участники:</b>\n<blockquote>{data}</blockquote>"

        await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=text_to_send), reply_markup=stop_view())
        #await message.answer(text_to_send, )
    else:
        #await bot.send_message(chat_id=message.chat.id, text='<b>Вы еще не вносили участников!</b>')
        text = '<b>Вы еще не внесли ни одного участника</b>'
        await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=text))
        await asyncio.sleep(2)
        await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=main_text), reply_markup=user_main_keyboard())
    await call.answer()

@add_time_fichi_handlers.callback_query(F.data == 'завершить_просмотр')
async def get_added_users(call: CallbackQuery):
    await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=main_text),
                                  reply_markup=user_main_keyboard())
    await call.answer()
