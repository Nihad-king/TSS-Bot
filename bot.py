import discord
from discord.ext import commands
import os

# Intents aktivieren
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Bot erstellen
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
GUILD_ID = 123456789012345678  
LOG_CHANNEL_ID = 123456789012345678  

@bot.event
async def on_ready():
    print(f"✅ {bot.user} ist online!")

    # Server und Channel holen
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Server not found. Check GUILD_ID.")
        return

    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        print("❌ Channel not found. Check LOG_CHANNEL_ID.")
        return

    try:
        await log_channel.send(f"🟢 {bot.user.name} ist jetzt online!")
        print("✅ Nachricht wurde im Discord-Channel gesendet.")
    except Exception as e:
        print(f"❌ Error sending: {e}")


bot.run(os.getenv("TOKEN"))
