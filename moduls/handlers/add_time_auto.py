import asyncio

from aiogram import Bot, Router, F, html
from aiogram.types import Message
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto
from moduls.other.static import main_text, main_photo_path, notes, notes_auto
import logging
from moduls.keyboards.main_keyboard import back_keyboard, user_main_keyboard
from moduls.keyboards.time_key import start_keyboard, finish_keyboard
from moduls.utils.states_form import StepsTimeAuto
from aiogram.fsm.context import FSMContext
from datetime import datetime

add_time_auto_handlers = Router(name=__name__)



@add_time_auto_handlers.callback_query(F.data == 'автомат')
async def select_auto_time(call: CallbackQuery, state: FSMContext):

    await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=notes_auto))
    await call.message.answer('<b>Введите номер участника:</b>')

    logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} выбрал указать время старта/финиша')
    await call.answer()
    await state.set_state(StepsTimeAuto.GET_ID)


@add_time_auto_handlers.message(StepsTimeAuto.GET_ID)
async def get_id(message: Message, state: FSMContext):

    if not message.text.isdigit():

        text = (f'<b>Введен не правильный формат!\n'
                f'Нормер участника должен быть числом!\n\n'
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
    start = datetime.now()
    await state.update_data(start=start)

    context_data = await state.get_data()
    id = context_data.get('id')

    await call.message.edit_text(f'<b>⏱️ Засекается время!</b>'
                                 f'<blockquote>Номер участника - <b>{id}</b>\n'
                                 f'Для завершения нажмите кнопку <b>ФИНИШ</b></blockquote>', reply_markup=finish_keyboard())
    await state.set_state(StepsTimeAuto.GET_FINISH)
    await call.answer()

@add_time_auto_handlers.callback_query(StepsTimeAuto.GET_FINISH)
async def get_finish(call: CallbackQuery, state: FSMContext):
    context_data = await state.get_data()
    start = context_data.get('start')
    id = context_data.get('id')

    finish = datetime.now()
    total_time = str((finish-start)).replace('.', ':')[2:10]
    data_user = (f'<b>Данные успешно занесены!</b>\n'
                 f'<blockquote>ID участника - <b>{id}</b>\n'
                 f'Время участника - <b>{total_time}</b></blockquote>\n')
    await call.message.edit_text(text=data_user)
    await asyncio.sleep(2)
    await call.message.answer_photo(photo=FSInputFile(path=main_photo_path), caption=main_text, reply_markup=user_main_keyboard())
    await call.answer()
    await state.clear()


