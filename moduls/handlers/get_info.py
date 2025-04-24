from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from moduls.keyboards.info_key import info_keyboard
from moduls.settings import settings
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
from moduls.other.static import token_sheet
from moduls.utils.additional import print_stat

info_handlers = Router(name=__name__)
ADMIN_CHANNEL = settings.bots.admin_channel

category_names = ['Категория А', 'Категория В', 'Категория С']
ages_names = ['10-13 лет', '14-17 лет', '🔙 Назад']

id_table = '1zYjSJhbwD_lwWMIYx4h7uJC6YIuWkzlmDzDhWBP1dX4'
google_sheet_info = GoogleSheet(token_sheet, id_table)


@info_handlers.message(F.text.lower() == 'инфо')
async def get_info(message: Message):
    range_name = 'Статистика!C6:F13'
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = ['<b>Общая статистика соревнований 🌀</b>\n']

    data_info_send += print_stat(data_info)
    data_info_send += ['\n<b>Для статистики по категориями нажмите одну из кнопок ниже👇</b>']

    data_info_send = '\n'.join(data_info_send)

    await message.answer(data_info_send, reply_markup=info_keyboard(category_names))


@info_handlers.callback_query(F.data == 'Категория А')
async def get_category_A(call: CallbackQuery):
    #await call.message.edit_reply_markup()
    range_name = 'Статистика!H6:I13'
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = [f'<b>{call.data}</b>\n']

    data_info_send += print_stat(data_info)
    if ':' in data_info_send[2]:
        data_info_send = '\n'.join(data_info_send)
        await call.message.answer(data_info_send)
    else:
        await call.message.answer(f'Участников на дистанции <b>{call.data}</b> еще не было')

    await call.answer()


@info_handlers.callback_query(F.data == 'Категория В')
async def get_category_A(call: CallbackQuery):
    #await call.message.edit_reply_markup()
    range_name = 'Статистика!K6:L13'
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = [f'<b>{call.data}</b>\n']

    data_info_send += print_stat(data_info)
    if ':' in data_info_send[2]:
        data_info_send = '\n'.join(data_info_send)
        await call.message.answer(data_info_send)
    else:
        await call.message.answer(f'Участников на дистанции <b>{call.data}</b> еще не было')

    await call.answer()


@info_handlers.callback_query(F.data == 'Категория С')
async def get_category_C(call: CallbackQuery):
    range_name = 'Статистика!C18:E22'
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = [f'<b>{call.data}</b>\n']

    data_info_send += print_stat(data_info)
    data_info_send += ['\n<b>Для статистики по возрастам категории С нажмите одну из кнопок ниже👇</b>']
    if ':' in data_info_send[2]:
        data_info_send = '\n'.join(data_info_send)
        await call.message.answer(data_info_send, reply_markup=info_keyboard(ages_names))
    else:
        await call.message.answer(f'Участников на дистанции <b>{call.data}</b> еще не было')

    await call.answer()


@info_handlers.callback_query(F.data == '10-13 лет')
async def get_category_C_10_13(call: CallbackQuery):
    #await call.message.edit_reply_markup()
    range_name = 'Статистика!H18:I22'
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = [f'<b>{call.data}</b>\n']

    data_info_send += print_stat(data_info)
    if ':' in data_info_send[2]:
        data_info_send = '\n'.join(data_info_send)
        await call.message.answer(data_info_send)
    else:
        await call.message.answer(f'Участников на дистанции <b>{call.data}</b> еще не было')

    await call.answer()


@info_handlers.callback_query(F.data == '14-17 лет')
async def get_category_C_14_17(call: CallbackQuery):
    #await call.message.edit_reply_markup()
    range_name = 'Статистика!K18:L22'
    data_info = google_sheet_info.read_data(range_name)

    data_info = [line for line in data_info if line]
    data_info_send = [f'<b>{call.data}</b>\n']

    data_info_send += print_stat(data_info)
    if ':' in data_info_send[2]:
        data_info_send = '\n'.join(data_info_send)
        await call.message.answer(data_info_send)
    else:
        await call.message.answer(f'Участников на дистанции <b>{call.data}</b> еще не было')

    await call.answer()

@info_handlers.callback_query(F.data == '🔙 Назад')
async def get_back_from_C(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=info_keyboard(category_names))


info_handlers.message.filter(F.chat.type.in_({"group", "supergroup"}))