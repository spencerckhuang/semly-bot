from nextcord.ext import commands, tasks
from datetime import datetime
import pytz
from reminder import (
    is_30_minutes_before_check_in,
    is_30_minutes_before_hack_session,
    is_check_in_time,
    is_hack_session_time,
)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reminder.start()

    @tasks.loop(seconds=30)
    async def reminder(self):
        channel = self.get_channel(939658799059451904)
        now = datetime.now(pytz.timezone("America/New_York"))
        if is_30_minutes_before_check_in(now):
            await channel.send("@everyone Week.ly Check-in in 30 minutes!")
        elif is_check_in_time(now):
            await channel.send("@everyone Week.ly Check-in now!")
        elif is_30_minutes_before_hack_session(now):
            await channel.send("@everyone Week.ly Hack Session in 30 minutes!")
        elif is_hack_session_time(now):
            await channel.send("@everyone Week.ly Hack Session now!")
        print(f"Looped: {now}")

    @reminder.before_loop
    async def before_reminder(self):
        await self.wait_until_ready()
