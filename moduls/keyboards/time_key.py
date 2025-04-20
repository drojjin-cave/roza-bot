from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def time_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='✅ Подтвердить', callback_data='подтвердить')
    keyboard_builder.button(text='⏱️ Изменить время', callback_data='изменить_время')
    keyboard_builder.button(text='🔢 Изменить номер', callback_data='изменить_номер')

    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup()

def start_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🏃‍♂️‍➡️ СТАРТ', callback_data='старт')

    return keyboard_builder.as_markup()

def finish_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🏁 ФИНИШ', callback_data='финиш')


    keyboard_builder.adjust(1,)
    return keyboard_builder.as_markup()

def stop_view():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🔙 Завершить просмотр', callback_data='завершить_просмотр')

    return keyboard_builder.as_markup()

def confirm_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='✅ Подтвердить', callback_data='подтвердить_финиш')
    keyboard_builder.button(text='🚫 Превышено КВ', callback_data='КВ')
    keyboard_builder.button(text='❌ Ошибка во времени', callback_data='данные не верны')


    keyboard_builder.adjust(1, )
    return keyboard_builder.as_markup()

def confirm_KB_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='✅ Подтвердить', callback_data='подтвердить_кв')
    keyboard_builder.button(text='❌ Отменить', callback_data='отменить_кв')

    return keyboard_builder.as_markup()