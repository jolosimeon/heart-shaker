import discord
import asyncio
import os
from random import randint 
from discord.ext import commands

from urllib import parse
import psycopg2
import re

keywordList = {}
cur = None
forbidden = {'set', 'list', 'remove'}
bot = commands.Bot(command_prefix="//", description="you're my heart shaker shaker")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #bot.load_extension("Keywords")
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
    if msg.content.startswith('//'):
        word = msg.content
        re.sub('//','', word, 1)
        print(word)
        if (keywordList.get(word) is not None):
            await bot.send_message(msg.channel, keywordList[word], tts=True)
        else:
            await bot.process_commands(msg)

@bot.command()
async def refresh():
    loadCommands()

@bot.command()
async def view():
    viewList = "**Commands:** \n"
    for key, value in keywordList.items():
        viewList += "`" + str(key) + "` " + str(value) + "\n"
    await bot.say(viewList)

@bot.command()
async def set(word, *, value=None):
    global keywordList
    if word is None:
        await self.bot.say("set wat")
    elif value is None:
        await self.bot.say("wat should I say")
    elif word in forbidden:
        await self.bot.say("cannot use dat keyword")
    else:
        if (keywordList.get(word) is not None):
            cur.execute("UPDATE heartshaker.keywords "
                        "SET value = %s"
                        "WHERE keyword = %s", (str(value), str(word)))
            await self.bot.say("Updated") 
        else:
            cur.execute("INSERT INTO heartshaker.keywords "
                        "VALUES (%s, %s)", (str(word), str(value)))
            await self.bot.say("New command added") 
        keywordList[word] = value

@bot.command()
async def remove(word):
    global keywordList
    if word is None:
        await self.bot.say("nothing to remove")
    elif word in forbidden:
        await self.bot.say("cannot remove dat")
    elif (keywordList.get(str(word)) is None):
        await self.bot.say(str(word) + " does not exist")
    else:
        print(word)
        cur.execute("DELETE FROM heartshaker.keywords "
                    "WHERE keyword = %s", (word))
        keywordList.pop(word)
        await self.bot.say("Command deleted") 

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
    cur.execute("SELECT * FROM heartshaker.keywords;")
    resultList = cur.fetchall()
    global keywordList
    keywordList = {}
    for row in resultList:
        keywordList[row[0]] = row[1]
#async def on_message(message):
    ##await bot.send_message(message.channel, 'sollenda me likey likey', tts=True)

##bot.run(os.getenv('TOKEN'))
bot.loop.create_task(status_loop())
bot.run(os.getenv('DEV-TOKEN'))