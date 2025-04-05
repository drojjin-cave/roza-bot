import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from moduls.handlers.basic import basic_handlers
from moduls.handlers.add_time_hand import add_time_hand_handlers
from moduls.handlers.add_time_auto import add_time_auto_handlers
from moduls.handlers.other_messages import other_messages_handlers

from moduls.settings import settings

dp = Dispatcher()


async def main():
    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_routers(basic_handlers,
                       add_time_hand_handlers,
                       add_time_auto_handlers,
                       other_messages_handlers)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s : [%(levelname)s] [%(name)s] : %(message)s")
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    asyncio.run(main())
