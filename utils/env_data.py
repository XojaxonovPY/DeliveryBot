from dotenv import load_dotenv
from os import getenv
from utils.settings import Env_path
load_dotenv(Env_path)
class BotConfig:
    TOKEN=getenv('BOT_TOKEN')
    PAYMENT_CLICK_TOKEN=getenv('PAYMENT_CLICK_TOKEN')
class DBConfig:
    DP_NAME=getenv('DP_NAME')
    DP_USER=getenv('DP_USER')
    DP_PASSWORD=getenv('DP_PASSWORD')
    DP_HOST=getenv('DP_HOST')
    DP_PORT=getenv('DP_PORT')
    DP_ASYNC_URL=getenv('DP_ASYNC_URL')
    DP_URL=getenv('DP_SYNC_URL')
class WebConfig:
    ADMIN_USERNAME=getenv('ADMIN_USERNAME')
    ADMIN_PASSWORD=getenv('ADMIN_PASSWORD')
class Config:
    bot=BotConfig()
    dp=DBConfig()
    web=WebConfig()