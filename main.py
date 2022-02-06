
from bot import Bot


bot = Bot(command_prefix="$")
with open("token.txt", mode="r") as f:
    bot.run(f.read())
