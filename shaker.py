import discord
import asyncio
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('//'):
        print(message.author.name + ' ' + str(message.timestamp))
    if message.content.startswith('//is sana gay?'):
        await client.send_message(message.channel, 'yeah i am so gay', tts=True)
    if message.content.startswith('//aw'):
        await client.send_message(message.channel, 'arvayne weak', tts=True)
    if message.content.startswith('//will'):
        await client.send_message(message.channel, 'kamusta naman', tts=True)
    if message.content.startswith('//jay'):
        await client.send_message(message.channel, 'jaylica likes girls', tts=True)
    if message.content.startswith('//john'):
        await client.send_message(message.channel, 'o rey wah... ow chin chin gha dice key nan da yo', tts=True)
    if message.content.startswith('//kain'):
        await client.send_message(message.channel, 'kain ano', tts=True)
    #    counter = 0
    #     tmp = await client.send_message(message.channel, 'Calculating messages...')
    #     async for log in client.logs_from(message.channel, limit=100):
    #         if log.author == message.author:
    #             counter += 1

    #     await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    # elif message.content.startswith('!sleep'):
    #     await asyncio.sleep(5)
    #     await client.send_message(message.channel, 'Done sleeping')

client.run(os.getenv('TOKEN'))

# from discord.ext import commands

# bot = commands.Bot(description="is sana gay", command_prefix="//")

# @bot.command()
# async def aw():
#     """This is the command's description.
#     This can span multiple lines."""
#     await bot.send_message(message.channel, 'arvayne weak', tts=True)
# @bot.command()
# async def say(*, something):
#     await bot.say(something)

# bot.run("")
