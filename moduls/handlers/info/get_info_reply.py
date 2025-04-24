from aiogram import Router, F
from aiogram.types import Message

from moduls.keyboards.info_key import info_reply_keyboard
from moduls.settings import settings
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
from moduls.other.static import token_sheet
from moduls.utils.additional import print_stat

info_reply_handlers = Router(name=__name__)
ADMIN_CHANNEL = settings.bots.admin_channel

category_names = {'Общая статистика': 'Статистика!C6:F13',
                  'Категория А': 'Статистика!H6:I13',
                  'Категория В': 'Статистика!K6:L13',
                  'Категория С': 'Статистика!C18:E22',
                  'Категория С 10-13': 'Статистика!H18:I22',
                  'Категория С 14-17': 'Статистика!K18:L22'}

id_table = '1zYjSJhbwD_lwWMIYx4h7uJC6YIuWkzlmDzDhWBP1dX4'
google_sheet_info = GoogleSheet(token_sheet, id_table)


@info_reply_handlers.message(F.text.lower() == 'статистика')
async def get_static_keyboard(message: Message):
    await message.answer('Статистика ВС 2025', reply_markup=info_reply_keyboard(category_names))


@info_reply_handlers.message(F.text == 'Общая статистика')
async def get_info(message: Message):
    range_name = 'Статистика!C6:F13'
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = [f'<b>{message.text}</b>']

    data_info_send += print_stat(data_info)

    data_info_send = '\n'.join(data_info_send)

    await message.answer(data_info_send)

@info_reply_handlers.message(F.text.in_(category_names))
async def get_info_category(message: Message):

    range_name = category_names[message.text]
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = [f'<b>{message.text}</b>']

    data_info_send += print_stat(data_info)
    if ':' in data_info_send[2]:
        data_info_send = '\n'.join(data_info_send)
        await message.answer(data_info_send)
    else:
        await message.answer(f'Участников на дистанции <b>{message.text}</b> еще не было')

info_reply_handlers.message.filter(F.chat.type.in_({"group", "supergroup"}))

