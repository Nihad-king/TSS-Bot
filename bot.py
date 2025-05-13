import discord
from discord.ext import commands
from keep_alive import keep_alive
from activity_tracker import setup as setup_tracker
from bot_music import setup as setup_music  # 👈 Hier importieren
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

setup_music(bot)  # 👈 Musik-Befehle registrieren

# IDs
GUILD_ID = 1167097735133016106
LOG_CHANNEL_ID = 1310346537381007370
INFO_CHANNEL_ID = 1167168385180782754
TOP_ROLE_NAME = "Real Active God"

@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")
    guild = bot.get_guild(GUILD_ID)
    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f"🟢 {bot.user.name} ist jetzt online!")

    setup_tracker(bot, GUILD_ID, TOP_ROLE_NAME, INFO_CHANNEL_ID)

keep_alive()
bot.run(os.getenv("TOKEN"))