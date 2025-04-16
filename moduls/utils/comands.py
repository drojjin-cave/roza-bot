from aiogram import Bot
from aiogram.types import Message
from aiogram.types import BotCommand, BotCommandScopeDefault
from moduls.settings import settings

ADMINS_ROZA = settings.bots.admins_roza

user_commands = [
    BotCommand(
        command="start",
        description='Перезапустить бота'
    ),
    BotCommand(
        command="help",
        description='Помощь/сообщить об ошибке'
    ),
    BotCommand(
        command="send_protocol",
        description='Отправить протокол'
    )

]

admin_commands = [
    BotCommand(
        command="start",
        description='Перезапустить бота'
    ),
    BotCommand(
        command="logs",
        description='Логи'
    )
]


async def set_commands(bot: Bot, id):
    if id in ADMINS_ROZA:
        await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
    else:
        await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())


