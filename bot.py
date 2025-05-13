import discord
from discord.ext import commands
import os
from bot_music import setup as setup_music  # Musikfunktionen aus externer Datei

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} ist online!")

# Setup externe Befehle
setup_music(bot)  # Musikkommandos werden hier hinzugefügt

# Bot starten
bot.run(os.getenv("TOKEN"))
