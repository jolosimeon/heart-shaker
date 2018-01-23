import discord
import asyncio
import os
from random import randint 
from discord.ext import commands

from urllib import parse
import psycopg2
import re

prefix = "//"
keywordList = {}
cur = None
forbidden = {'set', 'remove'}
possible = {'refresh', 'view'}
bot = commands.Bot(command_prefix=prefix, description="you're my heart shaker shaker")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #bot.load_extension("Keywords")
    loadCommands()
    await bot.change_presence(game=discord.Game(name='TWICE - Heart Shaker'))

async def status_loop():
    await bot.wait_until_ready()
    while not bot.is_closed:
        playing = ["TWICE - Heart Shaker", "TWICE - Likey", "Overwatch", "Fortnite", "League of Legends", "Deceit", 
                    "TWICE - TT", "Warframe", "VRChat", "Runescape 3", "Doki Doki Literature Club!"]
        await bot.change_presence(game=discord.Game(name=playing[randint(0, len(playing)-1)]))
        await asyncio.sleep(60)

@bot.event
async def on_message(msg):
    if msg.content.startswith(prefix):
        word = msg.content
        word = re.sub(prefix,'', word, 1)
        if (keywordList.get(word) is not None):
            await bot.send_message(msg.channel, keywordList[word], tts=True)
        else:
            word = word.split(" ", 1)[0]
            if (word in forbidden):
                #Check if user has permission
                if (msg.channel.permissions_for(msg.author).administrator):
                    await bot.process_commands(msg)
                else:
                    await bot.say("need to be admin to use")
            else:
                await bot.process_commands(msg)
    elif "nsfw" in msg.content:
        await bot.add_reaction(msg, '<:jaylicaeat:367384830981177344>')
        await bot.add_reaction(msg, '<:baldippray:365815736095997952>')

@bot.command()
async def refresh():
    """Re-fetch commands from database"""
    loadCommands()
    await bot.say("Commands have been refreshed")

@bot.command()
async def view():
    """View list of available commands."""
    viewList = "**Commands:** \n"
    for key, value in keywordList.items():
        viewList += "`" + str(key) + "` " + str(value) + "\n"
    await bot.say(viewList)

@bot.command()
async def set(word=None, *, value=None):
    """Set or update a new command"""
    global keywordList
    if word is None:
        await bot.say("set wat")
    elif value is None:
        await bot.say("wat should I say")
    elif word in forbidden or word in possible:
        await bot.say("cannot use dat keyword")
    else:
        if (keywordList.get(word) is not None):
            cur.execute("UPDATE heartshaker.keywords "
                        "SET value = %s"
                        "WHERE keyword = %s", (str(value), str(word)))
            await bot.say("Updated") 
        else:
            cur.execute("INSERT INTO heartshaker.keywords "
                        "VALUES (%s, %s)", (str(word), str(value)))
            await bot.say("New command added") 
        keywordList[word] = value

@bot.command()
async def remove(word=None):
    """Remove a command"""
    global keywordList
    if word is None:
        await bot.say("nothing to remove")
    elif word in forbidden or word in possible:
        await bot.say("cannot remove dat")
    elif (keywordList.get(str(word)) is None):
        await bot.say(str(word) + " does not exist")
    else:
        cur.execute("DELETE FROM heartshaker.keywords "
                    "WHERE keyword = %s", (word,))
        keywordList.pop(word)
        await bot.say("Command deleted") 

def initCon():
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    conn.autocommit = True
    global cur
    cur = conn.cursor()
    
def loadCommands():
    initCon()
    cur.execute("SELECT * FROM heartshaker.keywords ORDER BY keyword ASC;")
    resultList = cur.fetchall()
    global keywordList
    keywordList = {}
    for row in resultList:
        keywordList[row[0]] = row[1]
#async def on_message(message):
    ##await bot.send_message(message.channel, 'sollenda me likey likey', tts=True)

##bot.run(os.getenv('TOKEN'))
bot.loop.create_task(status_loop())
bot.run(os.getenv('TOKEN'))