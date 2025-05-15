import discord
from discord.ext import tasks
import datetime

GUILD_ID = 1167097735133016106
ROLE_NAME = "Real Active God"

# Speichert, wann ein User dem VC beigetreten ist
voice_join_times = {}

# Speichert, wann ein User zuletzt im VC gesehen wurde
last_seen_in_vc = {}


def setup(bot):
    @bot.event
    async def on_ready():
        check_voice_activity.start(bot)

    @tasks.loop(seconds=60)
    async def check_voice_activity(bot):
        now = datetime.datetime.utcnow()
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            return

        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if not role:
            print(f"⚠️ Rolle '{ROLE_NAME}' nicht gefunden.")
            return

        current_vc_users = set()

        for vc in guild.voice_channels:
            members = [m for m in vc.members if not m.bot]
            if len(members) >= 2:
                for member in members:
                    current_vc_users.add(member.id)
                    # Wenn noch nicht gespeichert, jetzt speichern
                    if member.id not in voice_join_times:
                        voice_join_times[member.id] = now
                    # Wenn mehr als 3 Minuten im VC
                    elif (now - voice_join_times[member.id]).total_seconds() >= 180:
                        if role not in member.roles:
                            await member.add_roles(role)
                            print(f"✅ Rolle vergeben an {member.display_name}")
                    last_seen_in_vc[member.id] = now

        # Prüfen, ob jemand die Rolle verlieren sollte
        for member in guild.members:
            if member.bot:
                continue
            if role in member.roles:
                last_seen = last_seen_in_vc.get(member.id)
                if not last_seen or (now - last_seen).total_seconds() >= 600:
                    await member.remove_roles(role)
                    voice_join_times.pop(member.id, None)
                    last_seen_in_vc.pop(member.id, None)
                    print(f"❌ Rolle entfernt von {member.display_name}")
