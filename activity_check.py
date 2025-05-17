import discord
from discord.ext import tasks
from datetime import datetime, timedelta

# Konfigurierbare Werte
ROLE_NAME = "Real Active God"
MIN_VC_TIME = timedelta(minutes=3)
INACTIVE_TIMEOUT = timedelta(minutes=5)

# Speicherung der Voice-Aktivität
voice_times = {}
last_seen_in_vc = {}

@tasks.loop(seconds=60)
async def check_voice_activity(bot):
    for guild in bot.guilds:
        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if not role:
            continue

        for vc in guild.voice_channels:
            members = [m for m in vc.members if not m.bot]
            if len(members) >= 2:
                now = datetime.utcnow()
                for member in members:
                    if member.id not in voice_times:
                        voice_times[member.id] = now
                    elif now - voice_times[member.id] >= MIN_VC_TIME:
                        if role not in member.roles:
                            await member.add_roles(role)
                            print(f"Beförderung: {member} hat die Rolle erhalten.")

                            # Nachricht in den Beförderungskanal senden
                            channel = discord.utils.get(guild.text_channels, name="beförderung")
                            if channel:
                                await channel.send(f"{member.mention} wurde zur **{ROLE_NAME}** befördert 🏅")
            else:
                for member in vc.members:
                    last_seen_in_vc[member.id] = datetime.utcnow()

        # Entzug der Rolle bei Inaktivität
        now = datetime.utcnow()
        for member in guild.members:
            if role in member.roles:
                last_seen = last_seen_in_vc.get(member.id)
                if last_seen and now - last_seen >= INACTIVE_TIMEOUT:
                    await member.remove_roles(role)
                    print(f"{member} war zu lange nicht aktiv. Rolle entfernt.")
                    channel = discord.utils.get(guild.text_channels, name="beförderung")
                    if channel:
                        await channel.send(f"{member.mention} hat die **{ROLE_NAME}** Rolle verloren. ❌")

def setup(bot):
    check_voice_activity.change_interval(seconds=60)
    check_voice_activity.start(bot)