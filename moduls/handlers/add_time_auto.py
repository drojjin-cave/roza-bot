import asyncio

from aiogram import Bot, Router, F, html
from aiogram.types import Message
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from moduls.other.static import main_text, main_photo_path, notes, notes_auto, token_sheet
import logging
from moduls.keyboards.main_keyboard import back_keyboard, user_main_keyboard
from moduls.keyboards.time_key import start_keyboard, finish_keyboard, confirm_keyboard, confirm_KB_keyboard
from moduls.utils.states_form import StepsTimeAuto
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta, timezone
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
from moduls.handlers.basic import mes_start

add_time_auto_handlers = Router(name=__name__)

id_table = '1zYjSJhbwD_lwWMIYx4h7uJC6YIuWkzlmDzDhWBP1dX4'  # Весенние старты 2025
google_sheet = GoogleSheet(token_sheet, id_table)

steps_time = ['ФИНИШ', 'КВ']
data_user_confirm = ''

@add_time_auto_handlers.callback_query(F.data == 'автомат')
async def select_auto_time(call: CallbackQuery, state: FSMContext):

    await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=notes_auto))
    await call.message.answer('<b>Введите номер участника:</b>')

    logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} выбрал указать время старта/финиша')
    await call.answer()
    await state.set_state(StepsTimeAuto.GET_ID)


@add_time_auto_handlers.message(StepsTimeAuto.GET_ID)
async def get_id(message: Message, state: FSMContext):
    data = google_sheet.read_data('Данные')
    id_players = google_sheet.read_data('Участники!C2:C')

    if not message.text.isdigit():

        text = (f'<b>Введен не правильный формат!\n'
                f'Нормер участника должен быть числом!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)

        await state.set_state(StepsTimeAuto.GET_ID)
    elif google_sheet.search_user_from_id(message.text, data):
        text = (f'<b>Этот пользователь уже занесен в базу данных!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)
        await state.set_state(StepsTimeAuto.GET_ID)
    elif message.text not in id_players:
        text = (f'<b>Такой номер участника не зарегистрирован!\n\n'
                f'Введите номер повторно:</b>')

        await message.answer(text)
        await state.set_state(StepsTimeAuto.GET_ID)

    else:
        await state.update_data(id=message.text)

        await message.answer(f'<blockquote>Номер участника - <b>{message.text}</b>\n'
                             f'Для запуска нажмите кнопку <b>СТАРТ</b></blockquote>', reply_markup=start_keyboard())
        await state.set_state(StepsTimeAuto.GET_START)

@add_time_auto_handlers.callback_query(StepsTimeAuto.GET_START)
async def get_start(call: CallbackQuery, state: FSMContext):
    start = datetime.now(timezone.utc)
    await state.update_data(start=start)

    context_data = await state.get_data()
    id = context_data.get('id')
    time_to_message_start = (start + timedelta(hours=7, minutes=0)).strftime('%H:%M:%S')
    global mes_start_time
    mes_start_time = (f'<b>⏱️ Засекается время!</b>'
                     f'<blockquote>Номер участника - <b>{id}</b>\n'
                     f'Время старта - <b>{time_to_message_start}</b>\n'
                     f'Для завершения нажмите кнопку <b>ФИНИШ</b></blockquote>')

    await call.message.edit_text(mes_start_time, reply_markup=finish_keyboard())
    await state.set_state(StepsTimeAuto.GET_FINISH)
    await call.answer()

@add_time_auto_handlers.callback_query(StepsTimeAuto.GET_FINISH)
async def get_finish(call: CallbackQuery, state: FSMContext, bot: Bot):
    global data_user_confirm
    if call.data == 'финиш':
        finish = datetime.now(timezone.utc)
        await state.update_data(finish=finish)

        context_data = await state.get_data()
        start = context_data.get('start')
        id = context_data.get('id')

        total_time = str((finish-start)).replace('.', ':')[2:10]

        start = (start + timedelta(hours=7, minutes=0)).strftime('%H:%M:%S')
        finish = (finish + timedelta(hours=7, minutes=0)).strftime('%H:%M:%S')

        data_user_confirm = (f'<b>Проверьте данные участника и подтвердите!</b>\n'
                     f'<blockquote>ID участника - <b>{id}</b>\n'
                     f'Время старта - <b>{start}</b>\n'
                     f'Время финиша - <b>{finish}</b>\n'
                     f'Время участника - <b>{total_time}</b></blockquote>\n')
        await call.message.edit_text(text=data_user_confirm, reply_markup=confirm_keyboard())
        await state.set_state(StepsTimeAuto.CONFIRM)

@add_time_auto_handlers.callback_query(StepsTimeAuto.CONFIRM)
async def confirm_menu(call: CallbackQuery, state: FSMContext):
    context_data = await state.get_data()
    start = context_data.get('start')
    finish = context_data.get('finish')
    id = context_data.get('id')

    total_time = str((finish - start)).replace('.', ':')[2:10]
    start = (start + timedelta(hours=7, minutes=0)).strftime('%H:%M:%S')
    finish = (finish + timedelta(hours=7, minutes=0)).strftime('%H:%M:%S')

    time_input = (datetime.now(timezone.utc) + timedelta(hours=7, minutes=0)).strftime('%d.%m.%y %H:%M:%S')
    refery_id = call.from_user.id
    data = [[time_input, id, total_time, refery_id]]

    if call.data == 'КВ':
        await call.message.edit_text(data_user_confirm + '\n<b>Вы выбрали превышение КВ!\n'
                                                      '👇 Подтвердите ваши действия</b>', reply_markup=confirm_KB_keyboard())
        await state.set_state(StepsTimeAuto.CONFIRM_KB)

    elif call.data == 'подтвердить_финиш':
        data_from_sheet = google_sheet.read_data('Данные')

        if google_sheet.search_user_from_id(id, data_from_sheet):
            await call.message.edit_reply_markup()
            await call.message.answer('Что-то пошло не так, попробуйте заново 😔')
        else:
            google_sheet.write_data('Данные', data)
            logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} '
                         f'занес следующие данные кнопкой старт/финиш {data}')

            data_user = (f'<b>Данные успешно занесены!</b>\n'
                         f'<blockquote>ID участника - <b>{id}</b>\n'
                         f'Время старта - <b>{start}</b>\n'
                         f'Время финиша - <b>{finish}</b>\n'
                         f'Время участника - <b>{total_time}</b></blockquote>\n\n'
                         f'Через несколько секунд появится главное меню...')
            await call.message.edit_text(text=data_user)

            await asyncio.sleep(5)
            mes_start[0] = await call.message.answer_photo(photo=FSInputFile(path=main_photo_path), caption=main_text,
                                                           reply_markup=user_main_keyboard())

            await state.clear()
            await call.answer()

    elif call.data == 'данные не верны':
        await call.message.edit_reply_markup(None)
        await call.message.answer('<b>Вы заметили ошибку!\nВнесение данных приостановлено!\nВнесите время с секундомера вручную!</b>')
        logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} '
                     f'указал, что есть расхождения с секундомером и отменил ввод данных! {data}')

        await asyncio.sleep(5)
        mes_start[0] = await call.message.answer_photo(photo=FSInputFile(path=main_photo_path), caption=main_text,
                                                       reply_markup=user_main_keyboard())

        await state.clear()
        await call.answer()


@add_time_auto_handlers.callback_query(StepsTimeAuto.CONFIRM_KB)
async def confirm(call: CallbackQuery, state: FSMContext, bot: Bot):
    if call.data == 'подтвердить_кв':
        context_data = await state.get_data()

        id = context_data.get('id')
        total_time = 'превышено КВ'

        data_from_sheet = google_sheet.read_data('Данные')
        time_input = (datetime.now(timezone.utc) + timedelta(hours=7, minutes=0)).strftime('%d.%m.%y %H:%M:%S')
        refery_id = call.from_user.id

        data = [[time_input, id, total_time, refery_id]]

        if google_sheet.search_user_from_id(id, data_from_sheet):
            await call.message.edit_reply_markup()
            await call.message.answer('Что-то пошло не так, попробуйте заново 😔')
            await asyncio.sleep(3)
            await call.answer()

            mes_start[0] = await call.message.answer_photo(photo=FSInputFile(path=main_photo_path), caption=main_text,
                                                           reply_markup=user_main_keyboard())

        else:
            google_sheet.write_data('Данные', data)
            logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} '
                         f'подтвердил превышение КВ кнопкой старт/финиш, занесенные данные {data}')

            data_user = (f'<b>Данные успешно занесены!</b>\n'
                         f'<blockquote>Участник с номером <b>{id}</b>\n'
                         f'превысил контрольное время!</blockquote>\n\n'
                         f'Через несколько секунд появится главное меню...')
            await call.message.edit_text(text=data_user, reply_markup=None)
            await asyncio.sleep(4)
            await call.answer()

            mes_start[0] = await call.message.answer_photo(photo=FSInputFile(path=main_photo_path), caption=main_text,
                                                           reply_markup=user_main_keyboard())

            await state.clear()

    elif call.data == 'отменить_кв':

        await call.message.edit_text(data_user_confirm, reply_markup=confirm_keyboard())

        await state.set_state(StepsTimeAuto.CONFIRM)

        await call.answer()


