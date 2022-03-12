from nextcord.ext import commands, tasks
from datetime import datetime
import pytz


class EventSchedulerCog(commands.Cog):
    @property
    def DEV_CHANNEL(self):
        return self.bot.get_channel(938956251080044608)

    @property
    def CHECK_IN_CHANNEL(self):
        return self.bot.get_channel(938960725316100166)

    @property
    def HACK_SESSION_CHANNEL(self):
        return self.bot.get_channel(942783396042645575)

    @property
    def TEST_CHANNEL(self):
        return self.bot.get_channel(939658799059451904)

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.reminder.start()

    @tasks.loop(seconds=59)
    async def reminder(self):
        now = datetime.now(pytz.timezone("America/New_York"))
        if is_half_hour_before_check_in(now):
            await self.send_before_check_in_message()
        elif is_check_in_time(now):
            await self.send_check_in_message()
        elif is_hour_before_hack_session(now):
            await self.send_before_hack_session_message()
        elif is_hack_session_time(now):
            await self.send_hack_session_message()

    async def send_before_check_in_message(self):
        await self.CHECK_IN_CHANNEL.send(
            f"{self.ACTIVE_DEVS} Week.ly Check-in in 30 minutes!"
        )

    async def send_check_in_message(self):
        await self.CHECK_IN_CHANNEL.send(
            f"{self.ACTIVE_DEVS} Week.ly Check-in now!\n{self.CHECK_IN_TEMPLATE}"
        )

    async def send_before_hack_session_message(self):
        attendance_message = await self.DEV_CHANNEL.send(
            f"{self.ACTIVE_DEVS} Week.ly Hack Session in 1 hour! "
            "Please react with ✅ if you can make it, "
            "⌛ if you will be late, and ❌ if you can't make it."
        )
        await attendance_message.add_reaction("✅")
        await attendance_message.add_reaction("⏳")
        await attendance_message.add_reaction("❌")
        modality_message = await self.DEV_CHANNEL.send(
            "Additionally, please react with 🧑 if you will be attending in-person "
            "and 💻 if you will be attending remotely."
        )
        await modality_message.add_reaction("🧑")
        await modality_message.add_reaction("💻")

    async def send_hack_session_message(self):
        await self.HACK_SESSION_CHANNEL.send(
            f"{self.ACTIVE_DEVS} Week.ly Hack Session now!\n"
            f"Please check-in at {self.CHECK_IN_CHANNEL.mention}."
        )
        await self.CHECK_IN_CHANNEL.send(self.CHECK_IN_TEMPLATE)

    @reminder.before_loop
    async def before_reminder(self):
        await self.bot.wait_until_ready()


def is_half_hour_before_check_in(time: datetime) -> bool:
    return time.weekday() == 2 and time.hour == 10 and time.minute == 30


def is_check_in_time(time: datetime) -> bool:
    return time.weekday() == 2 and time.hour == 11 and time.minute == 0


def is_hour_before_hack_session(time: datetime) -> bool:
    return time.weekday() == 5 and time.hour == 13 and time.minute == 0


def is_hack_session_time(time: datetime) -> bool:
    return time.weekday() == 5 and time.hour == 14 and time.minute == 0
