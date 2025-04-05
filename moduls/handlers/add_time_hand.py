from aiogram import Bot, Router, F, html
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message, ChatPermissions
from moduls.other.static import main_text, main_photo_path, format_time, notes
import logging
from moduls.keyboards.main_keyboard import back_keyboard, user_main_keyboard
from moduls.keyboards.time_key import time_keyboard
from aiogram.fsm.context import FSMContext
from moduls.utils.states_form import StepsTimeHand
from re import match
from aiogram.exceptions import TelegramBadRequest

add_time_hand_handlers = Router(name=__name__)
mymessage = ''

@add_time_hand_handlers.callback_query(F.data == 'ручной')
async def select_hand_time(call: CallbackQuery, state: FSMContext):
    text = (f'Начинаем заполнять данные участника.\n'
            f'{notes.strip()}\n'
            f'<b>Введите номер участника:</b>')
    global mymessage
    mymessage = await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=text))

    logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} выбрал внести время в ручную')


    await state.set_state(StepsTimeHand.GET_ID)


@add_time_hand_handlers.message(StepsTimeHand.GET_ID)
async def get_id(message: Message, state: FSMContext, bot: Bot):
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    if not message.text.isdigit():

        text = (f'{notes.strip()}\n'
                f'<b>Введен не правильный формат!</b>\n\n'
                f'<blockquote>Нормер участника должен быть числом!\n'
                f'Введите номер участника повторно!</blockquote>')

        try:
            await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id, caption=text)
        except TelegramBadRequest:
            await message.delete()

        await state.set_state(StepsTimeHand.GET_ID)
    else:
        await state.update_data(id=message.text)
        await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id,
                                       caption=notes.strip() + html.bold('\nВведите время в формате:') + '\n' +
                                               html.blockquote(format_time.replace('Введите время в формате:', "").strip()))


        await state.set_state(StepsTimeHand.GET_TIME)

@add_time_hand_handlers.message(StepsTimeHand.GET_TIME)
async def get_time(message: Message, state: FSMContext, bot: Bot):
    try:
        check_delete = await message.delete()
    except TelegramBadRequest:
        pass

    pat = r'[0-5][0-9]:[0-5][0-9]:[0-9]?[0-9]?'

    if len(message.text) == 8 and bool(match(pat, message.text)):
        await state.update_data(time=message.text)

        context_data = await state.get_data()
        id, time = context_data.get('id'), context_data.get('time')
        data_user = (f'{notes.strip()}\n'
                     f'<b>Подтвердите введенные данные:</b>\n'
                     f'<blockquote>ID участника - <b>{id}</b>\n'
                     f'Время участника - <b>{time}</b></blockquote>\n')

        await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id,
                                       caption=data_user, reply_markup=time_keyboard())
        await state.set_state(StepsTimeHand.CHECK_DATA)
    else:
        await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id,
                                       caption=notes.strip() + '<b>\nНеправильный формат времени!</b>\n' + html.blockquote(format_time.strip()))

        await state.set_state(StepsTimeHand.GET_TIME)



@add_time_hand_handlers.message(StepsTimeHand.GET_ONLY_ID)
async def get_only_id(message: Message, state: FSMContext, bot: Bot):
    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    if not message.text.isdigit():
        text = (f'{notes.strip()}\n'
                f'<b>Введен не правильный формат!</b>\n\n'
                f'Нормер участника должен быть числом!\n'
                f'Введите номер участника повторно!')

        try:
            await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id, caption=text)
        except TelegramBadRequest:
            await message.delete()
        await state.set_state(StepsTimeHand.GET_ONLY_ID)
    else:
        await state.update_data(id=message.text)

        context_data = await state.get_data()
        id, time = context_data.get('id'), context_data.get('time')
        data_user = (f'{notes.strip()}\n'
                     f'<b>Подтвердите введенные данные:</b>\n'
                     f'<blockquote>ID участника - <b>{id}</b>\n'
                     f'Время участника - <b>{time}</b></blockquote>\n')
        await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id, caption=data_user, reply_markup=time_keyboard())
        await state.set_state(StepsTimeHand.CHECK_DATA)


@add_time_hand_handlers.callback_query(StepsTimeHand.CHECK_DATA)
async def get_chek(call: CallbackQuery, state: FSMContext, bot: Bot):
    context_data = await state.get_data()
    time_user = context_data.get('time')
    id_user = context_data.get('id')
    if call.data == 'изменить_время':

        await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path),
                                                      caption=notes.strip() + f'\nВведенное ранее время\n<code><b>{time_user}</b></code>\n' + html.bold('\nВведи время в формате:') + '\n' + html.blockquote(format_time.replace('Введи время в формате:', "").strip())))

        await state.set_state(StepsTimeHand.GET_TIME)

        await call.answer()
    elif call.data == 'изменить_номер':
        await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path),
                                                      caption=notes.strip() + f'\nВведенный ранее номер:\n<code>{id_user}</code>\n' + '<b>\nВведите номер участника:</b>'))

        await state.set_state(StepsTimeHand.GET_ONLY_ID)
        await call.answer()
    elif call.data == 'подтвердить':

        await call.answer('Данные подтверждены!')
        context_data = await state.get_data()


        print(context_data)  # TODO: Здесь данные заносятся в таблицу
        logging.info(f'Пользователь {call.from_user.username} {call.from_user.id} '
                     f'занес следующие данные в ручную {context_data}')

        await state.clear()
        await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=main_text), reply_markup=user_main_keyboard())




async def non_check(message: Message, state: FSMContext, bot: Bot):
    if message.text:
        await message.delete()
        context_data = await state.get_data()
        id, time = context_data.get('id'), context_data.get('time')
        data_user = (f'{notes.strip()}\n'
                     f'<b>Подтвердите введенные данные:</b>\n'
                     f'<blockquote>ID участника - <b>{id}</b>\n'
                     f'Время участника - <b>{time}</b></blockquote>\n')
        await bot.edit_message_caption(chat_id=message.chat.id, message_id=mymessage.message_id, caption=data_user,
                                       reply_markup=time_keyboard())
        await state.set_state(StepsTimeHand.CHECK_DATA)


