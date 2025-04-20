from aiogram.utils.keyboard import  InlineKeyboardBuilder

def info_keyboard(info_names):
    keyboard_builder = InlineKeyboardBuilder()

    for info_name in info_names:
        keyboard_builder.button(text=info_name, callback_data=info_name)

    keyboard_builder.adjust(2,)
    return keyboard_builder.as_markup()
