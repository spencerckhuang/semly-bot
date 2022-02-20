from reminder import Reminder
from anonymessage import AnonyMessageCog
from nextcord.ext import commands
from decouple import config


bot = commands.Bot(command_prefix="$")
bot.add_cog(Reminder(bot))
bot.add_cog(AnonyMessageCog(bot))
bot.run(config("TOKEN"))
