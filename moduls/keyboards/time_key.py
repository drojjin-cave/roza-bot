from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def time_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='✅ Подтвердить', callback_data='подтвердить')
    keyboard_builder.button(text='⏱️ Изменить время', callback_data='изменить_время')
    keyboard_builder.button(text='🔢 Изменить номер', callback_data='изменить_номер')

    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()