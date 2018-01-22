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
        playing = ["TWICE - Heart Shaker", "TWICE - Likey", "Overwatch", "Fortnite", "League of Legends", "Deceit", 
                    "TWICE - TT", "Warframe", "VRChat"]
        await bot.change_presence(game=discord.Game(name=playing[randint(0, len(playing)-1)]))
        await asyncio.sleep(60)

@bot.event
async def on_message(msg):
    #if msg.content.startswith('//'):
        word = str(msg)
        #re.sub('//','', word, 1)
        #if (keywordList.get(word) is not None):
            #await self.bot.send_message(msg.channel, keywordList[word], tts=True)
        #else:
        await bot.process_commands(msg)
#async def on_message(message):
    ##await bot.send_message(message.channel, 'sollenda me likey likey', tts=True)

##bot.run(os.getenv('TOKEN'))
bot.loop.create_task(status_loop())
bot.run(os.getenv('DEV-TOKEN'))