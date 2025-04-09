from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.filters import Command
import asyncio

from moduls.other.static import  token_sheet
from moduls.keyboards.time_key import stop_view
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet


add_time_fichi_handlers = Router(name=__name__)
google_sheet_fichi = GoogleSheet(token_sheet)

@add_time_fichi_handlers.message(Command('users'))
async def get_added_users(message: Message, bot: Bot):
    await message.delete()

    all_data = google_sheet_fichi.read_data('Данные')
    data_referee = google_sheet_fichi.search_referee(message.from_user.id, all_data)
    if data_referee:
        head = '<b>ID</b> <b>Время</b>'
        data = [head, '---------------']
        for user in data_referee:

            data.append(f'{user["ID"]} {user["Время"]}')

        text_to_send = f"<b>Введенные вами участники:</b>\n<blockquote>{'\n'.join(data)}</blockquote>"
        await message.answer(text_to_send, reply_markup=stop_view())
    else:
        #await bot.send_message(chat_id=message.chat.id, text='<b>Вы еще не вносили участников!</b>')
        my = await message.answer('<b>Вы еще не вносили участников!</b>')
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=my.message_id)


@add_time_fichi_handlers.callback_query(F.data == 'завершить_просмотр')
async def get_added_users(call: CallbackQuery):
    await call.message.delete()
    await call.answer()
