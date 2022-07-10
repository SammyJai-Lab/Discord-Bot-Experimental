'''General Imports'''
from os.path import exists
from os import getenv
import sys
import os
import time
import traceback

'''Discord Bot'''
import discord
from dotenv import load_dotenv
from discord.ext import commands

'''YouTube Downloader'''
from pytube import YouTube

'''Songsterr to gp'''
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()
from bs4 import BeautifulSoup
from js import getRevisionId

'''Help Command'''
from helpstr import help_str

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$amuel ')

bot. remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# --- Command Start

class YouTubeDownloader(commands.Cog):
    '''
    Downloads YouTube videos as mp3s.
    '''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def downloadYT(self, ctx, arg=""):
        try:
            try:
                yt = YouTube(arg)
            except:
                await ctx.send("```Invalid URL / Audio not availiable```")
                return

            video = yt.streams.filter(only_audio=True).first()

            out_file = video.download(output_path=".")

            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'

            cnt = 1

            while exists(new_file):
                new_file = base + str(cnt) + ".mp3"
                cnt += 1

            print(new_file)

            os.rename(out_file, new_file)

        except Exception as e:
            print(e)

        try:
            filename = new_file

            await ctx.send(file=discord.File(filename))

            os.remove(filename)

        except Exception as e:
            print(e)
            return

bot.add_cog(YouTubeDownloader(bot))

class SongsterrToGP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def downloadSongsterr(self, ctx, arg=""):
        try:

            SONGSTERR_URL = arg

            # Validate songsterr url

            if "https://www.songsterr.com/" not in SONGSTERR_URL:
                raise Exception("Invalid Songsterr URL")

            r = await asession.get(SONGSTERR_URL)

            revisionID = await r.html.arender(script=getRevisionId, wait=1, reload=False)

            XML_URL = f"https://www.songsterr.com/a/ra/player/songrevision/{revisionID}.xml"

            r = await asession.get(XML_URL)

            data = BeautifulSoup(r.text, "xml")

            GP_URL = data.find("attachmentUrl").text

            filename = GP_URL.split('/')[-1]

            r = await asession.get(GP_URL)

            open(filename, "wb").write(r.content)

            print(type(r))

            r.close()

            await ctx.send(file=discord.File(filename))

            os.remove(filename)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error:", e, exc_tb.tb_lineno)
            try:
                r.close()
                return
            except:
                return

bot.add_cog(SongsterrToGP(bot))

class ForFun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fart(self, ctx):
        try:
            voice_state = ctx.author.voice
            if str(type(voice_state)) != "<class 'NoneType'>":
                voice_channel = voice_state.channel
                print("Executing --FART in [Voice channel: " + str(voice_channel) + "]")
                ctx.send("Executing --FART in [Voice channel: " + str(voice_channel) + "]")
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="assets\\ffmpeg\\bin\\ffmpeg.exe", source="assets\\soundEffects\\mp3s_fartSoundEffect.mp3"))
                # Sleep while audio is playing.
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()
            else:
                print("Err: user is not in a voice channel")
        
        except Exception as e:
            await ctx.send("OOPS, " + str(e))
            print(e)
            return

bot.add_cog(ForFun(bot))

# --- Command End

# Basic Error Handling
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

# Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send('pong')

# Help Command
@bot.command()
async def help(ctx):

    await ctx.send("```" + help_str + "```")
    
bot.run(TOKEN)