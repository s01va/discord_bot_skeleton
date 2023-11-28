
import os
from dotenv import load_dotenv

load_dotenv()


class BotConfig:
    APP_NAME = os.getenv("BOT_NAME", "BotName")
    APP_ENV = os.getenv("BOT_ENV", "dev")   # dev, prod

    LOG_PATH = os.getenv("LOG_PATH", './logs/')

    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
    if APP_ENV == "dev":
        DISCORD_NORMAL_CHANNEL_ID = int(os.getenv("DISCORD_NORMAL_CHANNEL_ID_DEV"))
    elif APP_ENV == "prod":
        DISCORD_NORMAL_CHANNEL_ID = int(os.getenv("DISCORD_NORMAL_CHANNEL_ID"))


bot_config = BotConfig()
