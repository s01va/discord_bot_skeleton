# https://discordpy.readthedocs.io/en/v2.3.2/ext/commands/api.html
import os
import glob
import asyncio
import logging.config
from config.bot_config import BotConfig
import discord
from discord.ext import commands, tasks

# logging setting
logging_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "logging.conf")
os.makedirs(BotConfig.LOG_PATH, exist_ok=True)
logging.config.fileConfig(fname=logging_config_path,
                          disable_existing_loggers=True,
                          defaults={
                              'app_name': BotConfig.APP_NAME,
                              'log_path': f"{os.path.join(BotConfig.LOG_PATH,BotConfig.APP_NAME)}"
                          }
                          )

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=commands.DefaultHelpCommand())


async def load_extensions():
    logging.info("load extentions...")
    cogs_path = os.path.join("Cogs", "*")
    cogs = [cog_file[0:-3] for cog_file in glob.glob(cogs_path) if cog_file.endswith(".py")]
    for cog in cogs:
        await bot.load_extension(cog.replace(os.path.sep, '.'))
    logging.info("done.")


@tasks.loop(seconds=3600)
async def loop1():
    # loop something
    return


@bot.event
async def on_ready():
    if BotConfig.APP_ENV == "dev":
        logging.info("bot mode: DEV")
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="dev/test")) # name 하는 중
    else:
        logging.info("bot mode: PROD")
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Activity(type=discord.ActivityType.listening, name="!help")) # name 시청 중
    loop1.start()
    logging.info(f"{BotConfig.APP_NAME} is ready")


@bot.event
async def on_member_join(member):
    welcome_message = f"hello {member.name}"
    logging.info(f"{member} has joined.")
    await bot.get_channel(BotConfig.DISCORD_NORMAL_CHANNEL_ID).send(welcome_message)

    request_change_nickname_msg = ""

    def check(msg):
        return msg.author == member

    try:
        await member.send(request_change_nickname_msg)
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        new_nickname = msg.content
        await member.edit(nick=new_nickname)
        await member.send(f"새로운 닉네임 {new_nickname}으로 변경에 성공했습니다.")
    except asyncio.TimeoutError:
        request_change_nickname_timeout_msg = "\n시간이 초과되었습니다.\n\n서버 내 닉네임 변경 방법:\n1. 우측 멤버 바에서 자신의 닉네임 우클릭\n2. 서버 프로필 편집 클릭\n3. 서버 프로필 탭에서 서버 별명 변경"
        await member.send(request_change_nickname_timeout_msg)


async def main():
    try:
        async with bot:
            await load_extensions()
            await bot.start(BotConfig.DISCORD_BOT_TOKEN)
    except Exception as e:
        logging.info(e)
    finally:
        logging.info(f"{BotConfig.APP_NAME} is stopped.")


if __name__ == '__main__':
    asyncio.run(main())
