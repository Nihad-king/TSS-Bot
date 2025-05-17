import discord
from discord.ext import commands
import os
from activity_check import setup as setup_activity_check

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")
    
    # Setup für Voice-Activity-Check
    setup_activity_check(bot)

    # Nachricht in den Beförderungskanal senden
    channel = discord.utils.get(bot.get_all_channels(), name="beförderung")
    if channel:
        await channel.send("✅ Der Bot ist jetzt online!")

bot.run(os.getenv("TOKEN"))