from bot.dispatcher import dp
from bot.handlers.delivery_product import deliver
from bot.handlers.main_handler import main

dp.include_routers(
    *[main,deliver]
)
