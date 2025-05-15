import discord
from discord.ext import tasks
import asyncio
from datetime import datetime, timedelta

# Konfigurierbare Werte
ROLE_NAME = "Real Active God"
MIN_VC_TIME = timedelta(minutes=3)
INACTIVE_TIMEOUT = timedelta(minutes=10)

# Member-ID -> Join-Zeit
vc_join_times = {}

# Member-ID -> Letzte bekannte VC-Zeit
last_seen_in_vc = {}

def setup_activity_check(bot):
    @bot.event
    async def on_voice_state_update(member, before, after):
        guild = member.guild
        role = discord.utils.get(guild.roles, name=ROLE_NAME)

        now = datetime.utcnow()

        if after.channel and len(after.channel.members) > 1:
            vc_join_times[member.id] = now
            last_seen_in_vc[member.id] = now
        elif before.channel and not after.channel:
            last_seen_in_vc[member.id] = now

        await asyncio.sleep(1)  # kleiner Delay, damit die Rolle nicht zu schnell entfernt/gesetzt wird

    @tasks.loop(seconds=60)
    async def check_voice_activity():
        now = datetime.utcnow()

        for guild in bot.guilds:
            role = discord.utils.get(guild.roles, name=ROLE_NAME)
            if not role:
                continue

            for member in guild.members:
                voice = member.voice

                # Wenn Member im VC ist mit anderen und lang genug dabei
                if voice and voice.channel and len(voice.channel.members) > 1:
                    join_time = vc_join_times.get(member.id)
                    if join_time and now - join_time >= MIN_VC_TIME:
                        if role not in member.roles:
                            await member.add_roles(role)
                    last_seen_in_vc[member.id] = now

                # Wenn Member NICHT im VC ist
                elif member.id in last_seen_in_vc:
                    inactive_duration = now - last_seen_in_vc[member.id]
                    if inactive_duration >= INACTIVE_TIMEOUT:
                        if role in member.roles:
                            await member.remove_roles(role)
                            vc_join_times.pop(member.id, None)
                            last_seen_in_vc.pop(member.id, None)

    check_voice_activity.start()
