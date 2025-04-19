import logging
import traceback

from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile, Message, ErrorEvent

from moduls.settings import settings


from datetime import datetime, timedelta, timezone
ADMINS_ROZA = settings.bots.admins_roza
ADMIN_CHANNEL = settings.bots.admin_channel


admin_handlers = Router(name=__name__)



# @admin_handlers.error()
# async def error_handler(event: ErrorEvent, bot: Bot):
#
#
#     date_update_info = datetime.now(timezone.utc)
#     date_update_info = (date_update_info + timedelta(hours=7, minutes=0)).strftime('%d.%m.%Y %H:%M:%S')
#
#     error = traceback.format_exc()
#     start_last_stack = error.rfind('File')
#     error = error[start_last_stack:]
#
#
#     logging.error(f'Время ошибки - {date_update_info}\n {error}')
#     # logging.info(
#     #     f'Пользователь {message.from_user.username} {message.from_user.id} оплатил тариф "{message.successful_payment.invoice_payload.upper()}"')
#
#     text = (f'Возникла ошибка!\n'
#             f'Время - <b>{date_update_info}</b>\n\n'
#             f'<b>Ошибка:</b>\n'
#             f'<blockquote>{error}</blockquote>'
#             )
#
#     await bot.send_message(ADMIN_CHANNEL, text=text)