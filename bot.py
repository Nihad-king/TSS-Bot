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

# Deine Server- und Channel-IDs
GUILD_ID = 123456789012345678  # Ersetze mit deiner echten Server-ID
LOG_CHANNEL_ID = 123456789012345678  # Ersetze mit deiner Channel-ID für Statusnachricht

@bot.event
async def on_ready():
    print(f"✅ {bot.user} ist online!")

    # Server und Channel holen
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ Server nicht gefunden. GUILD_ID prüfen.")
        return

    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        print("❌ Channel nicht gefunden. LOG_CHANNEL_ID prüfen.")
        return

    try:
        await log_channel.send(f"🟢 {bot.user.name} ist jetzt online!")
        print("✅ Nachricht wurde im Discord-Channel gesendet.")
    except Exception as e:
        print(f"❌ Fehler beim Senden: {e}")


bot.run(os.getenv("TOKEN"))
