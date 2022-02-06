from reminder import Reminder
from nextcord.ext import commands
from decouple import config


bot = commands.Bot(command_prefix="$")
bot.add_cog(Reminder(bot))
bot.run(config("TOKEN"))
