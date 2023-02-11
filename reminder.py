from nextcord.ext import commands, tasks
from datetime import datetime
import pytz


class ReminderCog(commands.Cog):
    ACTIVE_DEVS = "<@&938959783510294619>"
    AUTHORIZED_USERS = [716199395913105428, 229732075203330049]

    CHECK_IN_TEMPLATE = (
        "```\n"
        "**What I've done so far:** \n"
        "**What I still have to finish:** \n"
        "**What's blocking me:** \n"
        "```"
    )

    CHECK_OUT_TEMPLATE = (
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
        self.disabled_this_week = False
        self.active = True
        self.reminder.start()

    @tasks.loop(seconds=59)
    async def reminder(self):
        if not self.active:
            return
        now = datetime.now(pytz.timezone("America/New_York"))
        if self.disabled_this_week:
            if is_post_hack_session_time(now):
                self.disabled_this_week = False
            return
        if is_check_in_time(now):
            await self.send_check_in_message()
        elif is_hour_before_hack_session(now):
            await self.send_before_hack_session_message()
        elif is_hack_session_time(now):
            await self.send_hack_session_message()
        elif is_post_hack_session_time(now):
            await self.send_check_out_message()

    async def send_check_in_message(self):
        await self.CHECK_IN_CHANNEL.send(
            "Please check-in with the following template:\n"
        )
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

    async def send_check_out_message(self):
        await self.CHECK_IN_CHANNEL.send(
            "Please check-out with the following template:\n"
        )
        await self.CHECK_IN_CHANNEL.send(
            f"{self.ACTIVE_DEVS} {self.CHECK_OUT_TEMPLATE}"
        )

    @reminder.before_loop
    async def before_reminder(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def activate(self, ctx: commands.Context):
        self.active = True
        await ctx.send("Activated reminders.")

    @commands.command()
    async def deactivate(self, ctx: commands.Context):
        self.active = False
        await ctx.send("Deactivated reminders.")

    @commands.command()
    async def disable_this_week(self, ctx: commands.Context):
        if ctx.author.id in self.AUTHORIZED_USERS:
            self.disabled_this_week = True
            await ctx.send("Disabled this week's reminders.")
        else:
            await ctx.send("You don't have permission to do that.")


def is_check_in_time(time: datetime) -> bool:
    return time.weekday() == 5 and time.hour == 18 and time.minute == 0


def is_hour_before_hack_session(time: datetime) -> bool:
    return time.weekday() == 1 and time.hour == 19 and time.minute == 0


def is_hack_session_time(time: datetime) -> bool:
    return time.weekday() == 1 and time.hour == 20 and time.minute == 0


def is_post_hack_session_time(time: datetime) -> bool:
    return time.weekday() == 1 and time.hour == 21 and time.minute == 0
