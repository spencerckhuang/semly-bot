from nextcord.ext import commands, tasks
from datetime import datetime
import pytz


class Reminder(commands.Cog):
    DEV_CHANNEL = 938956251080044608
    TEST_CHANNEL = 939658799059451904
    ACTIVE_DEVS = "<@&938959783510294619>"

    def __init__(self, bot):
        self.bot = bot
        self.reminder.start()

    @tasks.loop(seconds=30)
    async def reminder(self):
        channel = self.bot.get_channel(self.DEV_CHANNEL)
        now = datetime.now(pytz.timezone("America/New_York"))
        if is_30_minutes_before_check_in(now):
            await channel.send(f"{self.ACTIVE_DEVS} Week.ly Check-in in 30 minutes!")
        elif is_check_in_time(now):
            await channel.send(f"{self.ACTIVE_DEVS} Week.ly Check-in now!")
        elif is_30_minutes_before_hack_session(now):
            message = await channel.send(
                f"{self.ACTIVE_DEVS}> Week.ly Hack Session in 30 minutes! "
                "Please react with ✅ if you can make it, "
                "⌛ if you will be late, and ❌ if you can't make it."
            )
            await message.add_reaction("✅️")
            await message.add_reaction("⌛")
            await message.add_reaction("❌")
        elif is_hack_session_time(now):
            await channel.send("@everyone Week.ly Hack Session now!")
        print(f"Looped: {now}")

    @reminder.before_loop
    async def before_reminder(self):
        await self.bot.wait_until_ready()


def is_30_minutes_before_check_in(time: datetime) -> bool:
    return time.weekday() == 0 and time.hour == 10 and time.minute == 30


def is_check_in_time(time: datetime) -> bool:
    return time.weekday() == 0 and time.hour == 11 and time.minute == 0


def is_30_minutes_before_hack_session(time: datetime) -> bool:
    return time.weekday() == 3 and time.hour == 15 and time.minute == 30


def is_hack_session_time(time: datetime) -> bool:
    return time.weekday() == 3 and time.hour == 16 and time.minute == 0
