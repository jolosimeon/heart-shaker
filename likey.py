from urllib import parse
from random import randint
import asyncio
import os
from dotenv import load_dotenv
import re
import psycopg2
from discord.ext import commands
import discord

load_dotenv()

prefix = "//"

if os.getenv('PYTHON_ENV') == 'dev':
    prefix = "/?"
keywordList = {}
cur = None
forbidden = ['keyword', 'remove', 'refresh', 'view', 'morehelp', 'tulog']
bot = commands.Bot(command_prefix=prefix, description="you're my heart shaker shaker")
bot.remove_command('help')
nsfwTrigger = False
unsafeMsg = None
helpID = None
page = 0
perPage = 15

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #bot.load_extension("Keywords")
    loadCommands()
    await bot.change_presence(activity=discord.Game(name='TWICE - Heart Shaker'))

async def status_loop():
    await bot.wait_until_ready()
    while not bot.is_closed:
        playing = ["TWICE - Heart Shaker", "TWICE - Fancy", "VALORANT", "League of Legends", "Among Us", 
                    "TWICE - TT", "TWICE - More & More", "VRChat", "Old School Runescape", "Doki Doki Literature Club!"]
        await bot.change_presence(activity=discord.Game(name=playing[randint(0, len(playing)-1)]))
        await asyncio.sleep(60)

@bot.event
async def on_message(msg):
    # global nsfwTrigger
    # global unsafeMsg
    if msg.content.startswith(prefix):
        word = msg.content
        word = re.sub(prefix,'', word, 1)
        if (keywordList.get(word) is not None):
            talk = True
            if (checkIfUrl(keywordList[word])):
                talk = False
            await sendWithAuthor(msg, keywordList[word], talk)
        elif (word.isdigit()):
            if  (int(word) == 1):
                await sendWithAuthor(msg, "wait " + word + " minute", True)
            elif (int(word) > 1 and int(word) <= 60):
                await sendWithAuthor(msg, "wait " + word + " minutes", True)
        else:
            word = word.split(" ", 1)[0]
            if (word in forbidden):
                #Check if user has permission
                #if (msg.channel.permissions_for(msg.author).administrator):
                await bot.process_commands(msg)
                #else:
                    #await bot.send(msg.channel, "need to be admin to use")
            else:
                await bot.process_commands(msg)
    elif "nsfw" in msg.content:
        nsfwTrigger = True
        await bot.add_reaction(msg, ':jaylicaeat:367384830981177344')
        await bot.add_reaction(msg, ':baldippray:365815736095997952')
    # elif nsfwTrigger is True and msg.author.id == '232916519594491906' and unsafeMsg is None:
    #     unsafeMsg = msg
    #     nsfwTrigger = False
    # if msg.content == '<:jaylicaeat:367384830981177344>':
    #     await bot.delete_message(unsafeMsg)
    #     unsafeMsg = None

@bot.command()
async def refresh(ctx):
    """Re-fetch commands from database"""
    loadCommands()
    await ctx.send("commands refreshed")

@bot.command()
async def tulog(ctx, name=None):
    if name is not None:
        tulog = "Tulog nah " + name
        await sendWithAuthor(ctx.message, tulog, True)
    else:
        await ctx.send("sino matutulog")

async def sendWithAuthor(msg, content, talk):
    me = msg.guild.me
    if talk: 
        await me.edit(nick=msg.author.display_name)
    await msg.channel.send(content, tts=talk)
    await me.edit(nick="heart shaker")

@bot.command()
async def keyword(ctx, word=None, *, value=None):
    """Set or update a new command"""
    global keywordList
    if word is None:
        await ctx.send("wat u want")
    elif value is None:
        await ctx.send("wat should I say")
    elif word in forbidden:
        await ctx.send("cannot use dat keyword")
    elif value.startswith(prefix):
        await ctx.send("cannot make me say words with prefix")
    else:
        if keywordList.get(word) is not None:
            cur.execute("UPDATE heartshaker.keywords "
                        "SET value = %s"
                        "WHERE keyword = %s", (value, word))
            await ctx.send("Updated")
        else:
            cur.execute("INSERT INTO heartshaker.keywords "
                        "VALUES (%s, %s)", (word, value))
            await ctx.send("New command added")
        keywordList[word] = value

@bot.command()
async def remove(ctx, word=None):
    """Remove a command"""
    global keywordList
    if word is None:
        await ctx.send("nothing to remove")
    elif word in forbidden:
        await ctx.send("cannot remove dat")
    elif (keywordList.get(word) is None):
        await ctx.send(word + " does not exist")
    else:
        cur.execute("DELETE FROM heartshaker.keywords "
                    "WHERE keyword = %s", (word,))
        keywordList.pop(word)
        await ctx.send("command deleted") 

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

@bot.command(pass_context=True)
async def view(ctx):
    """View list of available commands."""
    await viewHelp(ctx)

@bot.command(pass_context=True)
async def help(ctx):
    """View list of available commands."""
    await viewHelp(ctx)

async def viewHelp(ctx):
    viewList = "**Commands:**\n"
    viewList += "`keyword <word/string> <value>` set or update a new command\n"
    viewList += "`remove <word/string>` remove a command\n"
    viewList += "`<integer 1-60>` wait \_\_\_ minutes\n"
    viewList += "`tulog <string>` Tulog nah \_\_\_\n\n"
    viewList += "**Custom Commands:**\n"
    for key, value in keywordList.items():
        if (checkIfUrl(value)):
            value = cleanValue(value)
        viewList += "`" + str(key) + "` " + str(value) + "\n"
    await ctx.message.channel.send(viewList)

async def viewAltHelp(ctx):
    msg = await makeHelp()
    await bot.add_reaction(msg, "⬅")
    await bot.add_reaction(msg, "➡")

    global helpID
    if helpID is not None:
        try:
            #TODO: migrate this msg = await bot.get_message(ctx.channel, msg.id)
            msg.clear_reactions()
        except Exception:
            pass
    helpID = msg.id

async def makeHelp():
    viewList = "Use `morehelp` for other commands\n\n"
    i = page * perPage
    while i < page * (perPage + 1) and i < len(keywordList):
        key = list(keywordList.keys())[i]
        value = list(keywordList.values())[i]
        if checkIfUrl(value):
            value = cleanValue(value)
        viewList += "`" + str(key) + "` " + str(value) + "\n"
        i += 1
    numPages = len(keywordList)/perPage
    if len(keywordList) % numPages > 0:
        numPages += 1
    embed = discord.Embed(title="Custom Commands", colour=discord.Colour(0xa64ae2), description=viewList)
    embed.set_footer(text="Page " + (page + 1) + "/" + numPages)
    return embed

@bot.command(pass_context=True)
async def morehelp(ctx):
    viewList = "**Commands:**\n"
    viewList += "`Prefix:` " + prefix + "\n"
    viewList += "`keyword <word/string> <value>` set or update a new command\n"
    viewList += "`remove <word/string>` remove a command\n"
    viewList += "`<integer 1-60>` wait ___ minutes\n"
    viewList += "`tulog <string>` Tulog nah ___"
    await bot.send(ctx.message.channel, viewList)

@bot.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    channel = reaction.message.channel
    global page
    numPages = len(keywordList)/perPage
    if len(keywordList) % numPages > 0:
        numPages += 1 
    if reaction.emoji == "⬅" and msg.id == helpID and not reaction.me:
        if page - 1 >= 0:
            page -= 1
            #TODO: migrate this msg = await bot.get_message(msg.channel, helpID)
            embed = await makeHelp()
            #TODO: migrate this bot.edit_message(msg, embed)

def cleanValue(value):
    words = value.split(' ')
    newValue = ''
    for word in words:
        if checkIfUrl(word):
            word = "<" + word + ">"
            newValue += word
    return newValue

def checkIfUrl(url):
    pattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if (pattern.search(url) is not None):
        return True
    else:
        return False

##bot.run(os.getenv('TOKEN'))
bot.loop.create_task(status_loop())
bot.run(os.getenv('TOKEN'))