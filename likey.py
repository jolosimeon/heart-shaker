import discord
import asyncio
import os

from discord.ext import commands


print("hey!")

bot = commands.Bot(command_prefix="//", description="you're my heart shaker shaker")

@bot.event
async def on_ready():
    print("I'm ready!")

@bot.event 
async def on_message(message):
    ##await bot.send_message(message.channel, 'sollenda me likey likey', tts=True)

##bot.run(os.getenv('TOKEN'))
bot.run(os.getenv('DEV-TOKEN'))