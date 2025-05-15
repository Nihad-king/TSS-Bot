import discord
from discord.ext import commands
import os

from activity_check import setup_activity_check

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Server- und Channel-IDs
GUILD_ID = 1167097735133016106
LOG_CHANNEL_ID = 1310346537381007370
TOP_ROLE_NAME = "Real Active God"

@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")
    guild = bot.get_guild(GUILD_ID)
    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f"🟢 {bot.user.name} ist jetzt online!")

    setup_activity_check(bot) 

bot.run(os.getenv("TOKEN"))
