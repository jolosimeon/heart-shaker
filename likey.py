import discord
import asyncio
import os

from discord.ext import commands

bot = commands.Bot(command_prefix="//", description="you're my heart shaker shaker")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.add_cog(Keywords(bot))
    await bot.change_presence(game=discord.Game(name='TWICE - Heart Shaker'))

#async def on_message(message):
    ##await bot.send_message(message.channel, 'sollenda me likey likey', tts=True)

##bot.run(os.getenv('TOKEN'))
bot.run(os.getenv('DEV-TOKEN'))