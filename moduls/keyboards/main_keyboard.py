from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def user_main_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='⏳ Указать СТАРТ/ФИНИШ', callback_data='автомат')
    keyboard_builder.button(text='📝 Внести данные вручную', callback_data='ручной')
    keyboard_builder.button(text='👀 Посмотреть участников', callback_data='просмотр')

    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup()


def back_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='🔙 Назад', callback_data='назад')

    keyboard_builder.adjust(1,)
    return keyboard_builder.as_markup()