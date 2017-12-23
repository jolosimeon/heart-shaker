import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('//is sana gay?'):
        await client.send_message(message.channel, 'yeah i am so gay', tts=True)
    if message.content.startswith('//aw'):
        await client.send_message(message.channel, 'arvayne weak', tts=True)
    if message.content.startswith('//will'):
        await client.send_message(message.channel, 'kamusta naman', tts=True)
    if message.content.startswith('//jay'):
        await client.send_message(message.channel, 'jaylica likes girls', tts=True)
    #    counter = 0
    #     tmp = await client.send_message(message.channel, 'Calculating messages...')
    #     async for log in client.logs_from(message.channel, limit=100):
    #         if log.author == message.author:
    #             counter += 1

    #     await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    # elif message.content.startswith('!sleep'):
    #     await asyncio.sleep(5)
    #     await client.send_message(message.channel, 'Done sleeping')

client.run("MzkzNjk0MTUwNDY3NTE4NDY0.DR5f2Q.E1Ta1yb-PjhzuH0HdAS5wTwg7lY")