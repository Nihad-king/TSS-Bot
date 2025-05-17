import discord
from discord.ext import tasks
from datetime import datetime, timedelta
from discord.utils import get

# Werte
ROLE_NAME = "Real Active God"
MIN_VC_TIME = timedelta(hours=4)
INACTIVE_TIMEOUT = timedelta(weeks=1)
LOG_CHANNEL_NAME = "beförderungen"

# Speicherdaten
joined_at = {}
last_seen_in_vc = {}

def setup(bot):
    check_voice_activity.start(bot)

@tasks.loop(seconds=60)
async def check_voice_activity(bot):
    for guild in bot.guilds:
        role = get(guild.roles, name=ROLE_NAME)
        log_channel = get(guild.text_channels, name=LOG_CHANNEL_NAME)

        if not role:
            print(f"⚠️ Rolle '{ROLE_NAME}' nicht gefunden in {guild.name}")
            continue

        for member in guild.members:
            voice = member.voice

            if voice and voice.channel and len(voice.channel.members) >= 2:
                last_seen_in_vc[member.id] = datetime.utcnow()
                if member.id not in joined_at:
                    joined_at[member.id] = datetime.utcnow()

                time_in_vc = datetime.utcnow() - joined_at[member.id]

                if time_in_vc >= MIN_VC_TIME and role not in member.roles:
                    await member.add_roles(role)
                    print(f"✅ {member} wurde befördert.")

                    if log_channel:
                        await log_channel.send(f"{member.mention} wurde zur **{ROLE_NAME}** befördert!🎖️")

            else:
                if member.id in last_seen_in_vc:
                    time_inactive = datetime.utcnow() - last_seen_in_vc[member.id]

                    if time_inactive >= INACTIVE_TIMEOUT:
                        if role in member.roles:
                            await member.remove_roles(role)
                            print(f"⬇️ {member} wurde degradiert.")

                            if log_channel:
                                await log_channel.send(f"{member.mention} hat die **{ROLE_NAME}**-Rolle verloren.⚠️")

                        joined_at.pop(member.id, None)
                        last_seen_in_vc.pop(member.id, None)