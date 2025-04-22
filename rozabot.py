import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from moduls.handlers.add_time_fichi import add_time_fichi_handlers
from moduls.handlers.adminka import admin_handlers
from moduls.handlers.basic import basic_handlers
from moduls.handlers.add_time_hand import add_time_hand_handlers
from moduls.handlers.add_time_auto import add_time_auto_handlers
from moduls.handlers.bot_chat_talk import bot_chat_talk_handlers
from moduls.handlers.mailing.send_message import mailing_handlers
from moduls.handlers.other_messages import other_messages_handlers

from moduls.settings import settings
from moduls.handlers.send_protokol import send_protokol_handlers

dp = Dispatcher()


async def main():
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_routers(basic_handlers,
                       add_time_hand_handlers,
                       add_time_auto_handlers,
                       add_time_fichi_handlers,
                       send_protokol_handlers,
                       admin_handlers,
                       bot_chat_talk_handlers,
                       mailing_handlers,
                       other_messages_handlers)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s : [%(levelname)s] [%(name)s] : %(message)s")
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    logging.getLogger("googleapiclient.discovery").setLevel(logging.WARNING)
    logging.getLogger("oauth2client.transport").setLevel(logging.WARNING)
    logging.getLogger("oauth2client.client").setLevel(logging.WARNING)
    asyncio.run(main())
