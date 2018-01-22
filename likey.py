import discord
import asyncio
import os
from random import randint 
from discord.ext import commands

bot = commands.Bot(command_prefix="//", description="you're my heart shaker shaker")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.load_extension("Keywords")
    await bot.change_presence(game=discord.Game(name='TWICE - Heart Shaker'))

async def status_loop():
    await bot.wait_until_ready()
    while not bot.is_closed:
        playing = ["TWICE - Heart Shaker", "TWICE - Likey", "Overwatch", "Fortnite", "League of Legends"]
        await bot.change_presence(game=discord.Game(name=playing[randint(0, 4)]))
        await asyncio.sleep(60)

#async def on_message(message):
    ##await bot.send_message(message.channel, 'sollenda me likey likey', tts=True)

##bot.run(os.getenv('TOKEN'))
bot.loop.create_task(status_loop())
bot.run(os.getenv('DEV-TOKEN'))