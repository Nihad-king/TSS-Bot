import discord
from discord.ext import commands
import yt_dlp

def setup(bot):
    @bot.command(name="play", help="Spielt Musik von einem YouTube-Link")
    async def play(ctx, url: str):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("⚠️ Du musst zuerst in einen Voice-Channel gehen.")
            return

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'default_search': 'auto',
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info['url']

        source = discord.FFmpegPCMAudio(
            stream_url,
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            options='-vn'
        )

            
        ctx.voice_client.stop()  # stop previous audio
        ctx.voice_client.play(source)

        await ctx.send(f"🎶 Jetzt spiele ich: **{info.get('title', 'Unbekannt')}**")

    @bot.command(name="leave", help="Bot verlässt den Voice-Channel")
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Bot hat den Voice-Channel verlassen.")
        else:
            await ctx.send("❌ Ich bin in keinem Voice-Channel.")


