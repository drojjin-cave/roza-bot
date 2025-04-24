from aiogram import Bot, Router, F, html
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message, ChatPermissions
from moduls.other.static import main_text, main_photo_path, format_time, notes
import logging
from moduls.keyboards.main_keyboard import back_keyboard, user_main_keyboard
from moduls.keyboards.time_key import time_keyboard
from aiogram.fsm.context import FSMContext
from moduls.utils.states_form import StepsTimeHand
from re import match
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
import asyncio
from datetime import datetime, timezone, timedelta
from moduls.other.static import token_sheet
from moduls.handlers.basic import mes_start

add_time_hand_handlers = Router(name=__name__)

id_table = '1zYjSJhbwD_lwWMIYx4h7uJC6YIuWkzlmDzDhWBP1dX4'  # Весенние старты 2025
google_sheet_hand = GoogleSheet(token_sheet, id_table)

@add_time_hand_handlers.callback_query(F.data == 'ручной')
async def select_hand_time(call: CallbackQuery, state: FSMContext):
    text = (f'Начинаем заполнять данные участника.\n'
            f'{notes.strip()}')
    global mymessage
    mymessage = await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=text))
    await call.message.answer('<b>Введите номер участника:</b>')
    logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} выбрал внести время в ручную')


    await state.set_state(StepsTimeHand.GET_ID)


@add_time_hand_handlers.message(StepsTimeHand.GET_ID)
async def get_id(message: Message, state: FSMContext, bot: Bot):
    data = google_sheet_hand.read_data('Данные')
    id_players = google_sheet_hand.read_data('Участники!C2:C')
    if not message.text.isdigit():

        text = (f'<b>Введен не правильный формат!\n'
                f'Нормер участника должен быть числом!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)

        await state.set_state(StepsTimeHand.GET_ID)
    elif google_sheet_hand.search_user_from_id(message.text, data):
        text = (f'<b>Этот пользователь уже занесен в базу данных!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)
        await state.set_state(StepsTimeHand.GET_ID)

    elif message.text not in id_players:
        text = (f'<b>Такой номер участника не зарегистрирован!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)
        await state.set_state(StepsTimeHand.GET_ID)
    else:
        await state.update_data(id=message.text)

        await message.answer(html.bold('\nВведите время в формате:') + '\n' +
                                               html.blockquote(format_time.replace('Введите время в формате:', "").strip()))
        await state.set_state(StepsTimeHand.GET_TIME)

@add_time_hand_handlers.message(StepsTimeHand.GET_TIME)
async def get_time(message: Message, state: FSMContext, bot: Bot):

    pat = r'[0-5][0-9]:[0-5][0-9]:[0-9]?[0-9]?'


    if int(message.text[-2:]) < 10:
        await message.answer('<b>Введено время менее 10 секунд, такого быть не должно!</b>\n' + html.blockquote(format_time.strip()))
        await state.set_state(StepsTimeHand.GET_TIME)

    elif len(message.text) == 8 and bool(match(pat, message.text)):
        await state.update_data(time=message.text)

        context_data = await state.get_data()
        id, time = context_data.get('id'), context_data.get('time')
        data_user = (f'<b>Подтвердите введенные данные:</b>\n'
                     f'<blockquote>ID участника - <b>{id}</b>\n'
                     f'Время участника - <b>{time}</b></blockquote>\n')

        # await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id,
        #                                caption=data_user, reply_markup=time_keyboard())
        await message.answer(data_user, reply_markup=time_keyboard())
        await state.set_state(StepsTimeHand.CHECK_DATA)
    else:
        # await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id,
        #                                caption=notes.strip() + '<b>\nНеправильный формат времени!</b>\n' + html.blockquote(format_time.strip()))
        await message.answer('<b>Неправильный формат времени!</b>\n' + html.blockquote(format_time.strip()))

        await state.set_state(StepsTimeHand.GET_TIME)



@add_time_hand_handlers.message(StepsTimeHand.GET_ONLY_ID)
async def get_only_id(message: Message, state: FSMContext, bot: Bot):
    data = google_sheet_hand.read_data('Данные')

    if not message.text.isdigit():
        text = (f'<b>Введен не правильный формат!\n'
                f'Нормер участника должен быть числом!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)
        await state.set_state(StepsTimeHand.GET_ONLY_ID)
    elif google_sheet_hand.search_user_from_id(message.text, data):
        text = (f'<b>Такой пользователь уже есть в базе!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)
        await state.set_state(StepsTimeHand.GET_ONLY_ID)
    else:
        await state.update_data(id=message.text)

        context_data = await state.get_data()
        id, time = context_data.get('id'), context_data.get('time')
        data_user = (f'<b>Подтвердите введенные данные:</b>\n'
                     f'<blockquote>ID участника - <b>{id}</b>\n'
                     f'Время участника - <b>{time}</b></blockquote>\n')
        await message.answer(data_user, reply_markup=time_keyboard())
        await state.set_state(StepsTimeHand.CHECK_DATA)


@add_time_hand_handlers.callback_query(StepsTimeHand.CHECK_DATA)
async def get_chek(call: CallbackQuery, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    time_user = context_data.get('time')
    id_user = context_data.get('id')
    if call.data == 'изменить_время':
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f'<blockquote>Введенное ранее время\n<code><b>{time_user}</b></code></blockquote>\n' +
                                  html.bold('\nВведи время в формате:') + '\n' +
                                  html.blockquote(format_time.replace('Введи время в формате:', "").strip()))

        await state.set_state(StepsTimeHand.GET_TIME)

        await call.answer()
    elif call.data == 'изменить_номер':
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.answer(f'<blockquote>Введенный ранее номер:\n<b>{id_user}</b></blockquote>\n' + '<b>\nВведите номер участника:</b>')

        await state.set_state(StepsTimeHand.GET_ONLY_ID)
        await call.answer()
    elif call.data == 'подтвердить':
        data = google_sheet_hand.read_data('Данные')
        time_input = (datetime.now(timezone.utc) + timedelta(hours=7, minutes=0)).strftime('%d.%m.%y %H:%M:%S')
        refery_id = call.from_user.id

        data_user = [[time_input, id_user, time_user, refery_id]]
        if google_sheet_hand.search_user_from_id(id_user, data):
            await call.message.edit_reply_markup()
            await call.message.answer('Что-то пошло не так, попробуйте заново 😔')
            await asyncio.sleep(3)
        else:
            google_sheet_hand.write_data('Данные', data_user)

            data_user_text = (f'<b>Данные успешно занесены!</b>\n'
                         f'<blockquote>ID участника - <b>{id_user}</b>\n'
                         f'Время участника - <b>{time_user}</b></blockquote>\n')
            await call.message.edit_text(text=data_user_text)
            await asyncio.sleep(2)
            await call.answer()

            logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} '
                         f'занес следующие данные в ручную {data_user}')

        await state.clear()
        mes_start[0] = await bot.send_photo(call.from_user.id, photo=FSInputFile(path=main_photo_path), caption=main_text, reply_markup=user_main_keyboard())



