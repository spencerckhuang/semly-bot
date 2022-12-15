from nextcord.ext import commands, tasks
from datetime import datetime
import pytz


class ReminderCog(commands.Cog):
    ACTIVE = True
    ACTIVE_DEVS = "<@&938959783510294619>"

    CHECK_IN_TEMPLATE = (
        "Please check-in with the following template:\n"
        "```\n"
        "**What I've done so far:** \n"
        "**What I still have to finish:** \n"
        "**What's blocking me:** \n"
        "```"
    )

    CHECK_OUT_TEMPLATE = (
        "Please check-out with the following template:\n"
        "```\n"
        "**What I'll do by the next meeting:** \n"
        "**What I foresee may slow my progress:** \n"
        "**Any feedback on last week's progress or today's meeting**: \n"
        "```"
    )

    @property
    def DEV_CHANNEL(self):
        return self.bot.get_channel(938956251080044608)

    @property
    def CHECK_IN_CHANNEL(self):
        return self.HACK_SESSION_CHANNEL

    @property
    def HACK_SESSION_CHANNEL(self):
        return self.bot.get_channel(942783396042645575)

    @property
    def TEST_CHANNEL(self):
        return self.bot.get_channel(939658799059451904)

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        if self.ACTIVE:
            self.reminder.start()

    @tasks.loop(seconds=59)
    async def reminder(self):
        now = datetime.now(pytz.timezone("America/New_York"))
        # if is_check_in_time(now):
            # await self.send_check_in_message()
        # elif is_hour_before_hack_session(now):
            # await self.send_before_hack_session_message()
        if is_hack_session_time(now):
            await self.send_hack_session_message()
        # elif is_post_hack_session_time(now):
            # await self.send_check_out_message()

    async def send_check_in_message(self):
        await self.CHECK_IN_CHANNEL.send(
            f"{self.ACTIVE_DEVS} Week.ly Check-in now!\n{self.CHECK_IN_TEMPLATE}"
        )

    async def send_before_hack_session_message(self):
        attendance_message = await self.HACK_SESSION_CHANNEL.send(
            f"{self.ACTIVE_DEVS} Week.ly Hack Session in 1 hour! "
            "Please react with ✅ if you can make it, "
            "⌛ if you will be late, and ❌ if you can't make it."
        )
        await attendance_message.add_reaction("✅")
        await attendance_message.add_reaction("⏳")
        await attendance_message.add_reaction("❌")
        modality_message = await self.HACK_SESSION_CHANNEL.send(
            "Additionally, please react with 🧑 if you will be attending in-person "
            "and 💻 if you will be attending remotely."
        )
        await modality_message.add_reaction("🧑")
        await modality_message.add_reaction("💻")

    async def send_hack_session_message(self):
        await self.HACK_SESSION_CHANNEL.send(
            f"{self.ACTIVE_DEVS} Week.ly Hack Session reminder!"
        )

    async def send_post_hack_session_message(self):
        await self.CHECK_IN_CHANNEL.send(
            f"{self.ACTIVE_DEVS} {self.CHECK_OUT_TEMPLATE}"
            ""
        )

    @reminder.before_loop
    async def before_reminder(self):
        await self.bot.wait_until_ready()


def is_check_in_time(time: datetime) -> bool:
    return time.weekday() == 6 and time.hour == 18 and time.minute == 0


def is_hour_before_hack_session(time: datetime) -> bool:
    return time.weekday() == 2 and time.hour == 18 and time.minute == 0


def is_hack_session_time(time: datetime) -> bool:
    return time.weekday() == 2 and time.hour == 19 and time.minute == 0


def is_post_hack_session_time(time: datetime) -> bool:
    return time.weekday() == 2 and time.hour == 20 and time.minute == 0
