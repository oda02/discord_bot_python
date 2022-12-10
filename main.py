import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, message_content=True, voice_states=True)
bot = commands.Bot(command_prefix='!', intents=intents)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)



async def setup():
    print("Running setup...")
    await bot.load_extension("cogs.music")
    # bot.add_cog(player.Music(bot))

    print("Setup complete.")


# @bot.command()
# async def ping(ctx):
#     await ctx.send('pong')


asyncio.run(setup())

bot.run(os.getenv('TOKEN'), reconnect=True)