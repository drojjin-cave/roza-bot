import asyncio

from aiogram import Router, html, F, Bot
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.filters import CommandStart, Command
import logging
from moduls.other.static import main_text, main_photo_path, help_text
from moduls.keyboards.main_keyboard import *
from aiogram.fsm.context import FSMContext

from moduls.utils.comands import set_commands
from moduls.utils.google_sheet.GoogleSheet import GoogleSheet
from moduls.other.static import token_sheet
from moduls.utils.states_form import Help

id_table = '1LjYgO3xAXoi1kC828beed1hBMTuDmOCt4iQvAUBqC84'  # База данных бота
google_sheet_base = GoogleSheet(token_sheet, id_table)

basic_handlers = Router(name=__name__)

mes_start = [None]

@basic_handlers.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot, state: FSMContext):
    await set_commands(bot, message.from_user.id)
    await state.clear()
    try:
        await bot.edit_message_reply_markup(message_id=mes_start[0].message_id, reply_markup=None, chat_id=message.chat.id)
    except:
        pass

    mes1 = await bot.send_photo(message.from_user.id, photo=FSInputFile(path=main_photo_path), caption=main_text, reply_markup=user_main_keyboard())
    mes_start[0] = mes1

    logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} нажал кнопку старт')

    id_users = google_sheet_base.read_data('Пользователи!A2:A')
    if str(message.from_user.id) not in id_users:

        data = [[message.from_user.id,
                 message.from_user.last_name,
                 message.from_user.first_name,
                 message.from_user.username,
                 'пользователь']]


        google_sheet_base.write_data('Пользователи!A2:E', data)
        logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} занесен в базу данных')



@basic_handlers.message(Command("help"))
async def get_help(message: Message, bot: Bot, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        try:
            await message.delete()
            await bot.edit_message_reply_markup(message_id=mes_start[0].message_id, reply_markup=None, chat_id=message.chat.id)
            await message.answer(help_text)

            #await bot.edit_message_caption(message_id=mes_start.message_id, reply_markup=None, chat_id=message.chat.id, caption=help_text)
            await state.set_state(Help.GET_HELP)
        except:
            await message.answer('Были обнаружены доработки, пожалуйста, перезапустите бота')


        #await bot.edit_message_reply_markup(message_id=mes_start.message_id, reply_markup=None, chat_id=message.chat.id)



@basic_handlers.message(Help.GET_HELP)
async def help_answer(message: Message, state: FSMContext, bot: Bot):

    text_answer = ('\nИнформация принята, отправлена администраторам и будет обработана в ближайшее время!\n'
                    'Спасибо за информацию!😏\n\n'
                   'Через несколько секунд появится главное меню...')
    await message.reply(text_answer)
    await state.clear()

    await asyncio.sleep(5)
    global mes_start
    mes_start[0] = await bot.send_photo(message.from_user.id, photo=FSInputFile(path=main_photo_path), caption=main_text,
                                     reply_markup=user_main_keyboard())










@basic_handlers.callback_query(F.data == 'назад')
async def back(call: CallbackQuery, bot: Bot):
    await call.message.edit_media(InputMediaPhoto(media=FSInputFile(path=main_photo_path), caption=main_text),
                                  reply_markup=user_main_keyboard())

    await call.answer()

basic_handlers.message.filter(F.chat.type == "private")