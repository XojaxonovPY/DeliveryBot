import asyncio
import logging
import sys

from aiogram.types import BotCommand

from bot.handlers import *
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from utils.env_data import BotConfig

TOKEN = BotConfig.TOKEN


# from db.model import db
# db.init()
# asyncio.run(db.create_all())
# import bcrypt
# print(bcrypt.hashpw("3".encode(), salt=bcrypt.gensalt()))

async def set_bot_commands(bot: Bot):
    commands = [BotCommand(command="/start", description="Starting bot."), ]
    await bot.set_my_commands(commands=commands)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
