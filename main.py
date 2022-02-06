from bot import Bot
from decouple import config


bot = Bot(command_prefix="$")
bot.run(config("TOKEN"))
