import discord
from discord.ext import commands
import yt_dlp
import os

def setup(bot):
    @bot.command()
    async def join(ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
                await ctx.send(f"🎧 Joined `{channel.name}`!")
            else:
                await ctx.voice_client.move_to(channel)
        else:
            await ctx.send("❗ Du musst zuerst einem Voice-Channel beitreten.")

    @bot.command()
    async def play(ctx, url):
        if not ctx.author.voice:
            await ctx.send("❗ Du musst in einem Voice-Channel sein.")
            return

        voice_client = ctx.voice_client
        if not voice_client:
            await ctx.author.voice.channel.connect()
            voice_client = ctx.voice_client

        # Download-Optionen
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': 'song.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        source = discord.FFmpegPCMAudio(
            filename,
            executable="ffmpeg",  # Render benutzt "ffmpeg", lokal ggf. Pfad anpassen
            options="-vn"
        )

        voice_client.play(source, after=lambda e: print(f"Song finished: {e}"))
        await ctx.send(f"▶️ Spiele jetzt: **{info['title']}**")

    @bot.command()
    async def stop(ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("⏹️ Musik gestoppt.")
        else:
            await ctx.send("❗ Ich bin nicht im Voice-Channel.")

    @bot.command()
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Verlasse den Voice-Channel.")
        else:
            await ctx.send("❗ Ich bin nicht im Voice-Channel.")
