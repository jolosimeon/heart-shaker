import discord
from discord.ext import commands

bot = commands.Bot(description="is sana gay", command_prefix="//")

@bot.command()
async def aw():
	"""This is the command's description.
    This can span multiple lines."""
	await bot.send_message(message.channel, 'arvayne weak', tts=True)
@bot.command()
async def say(*, something):
    await bot.say(something)

bot.run("MzkzNjk0MTUwNDY3NTE4NDY0.DR5f2Q.E1Ta1yb-PjhzuH0HdAS5wTwg7lY")