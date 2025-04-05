from aiogram import Router
from aiogram.types import Message

import logging

other_messages_handlers = Router(name=__name__)

@other_messages_handlers.message()
async def command_start_handler(message: Message):
    await message.delete()
    logging.info(f'Пользователь {message.from_user.username} {message.from_user.id} ввел неизвестное сообщение - "{message.text}"')




