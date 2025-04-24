from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

def info_keyboard(info_names):
    keyboard_builder = InlineKeyboardBuilder()

    for info_name in info_names:
        keyboard_builder.button(text=info_name, callback_data=info_name)

    keyboard_builder.adjust(2,)
    return keyboard_builder.as_markup()


def info_reply_keyboard(info_names):
    keyboard_builder = ReplyKeyboardBuilder()

    for info_name in info_names.keys():
        keyboard_builder.button(text=info_name, callback_data=info_name)

    keyboard_builder.adjust(1, 3, 2)
    return keyboard_builder.as_markup(resize_keyboard=True)
