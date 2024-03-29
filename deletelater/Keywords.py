import discord
from discord.ext import commands

import os
from urllib import parse
import psycopg2
import re

keywordList = {}
cur = None
forbidden = {'set', 'list', 'remove'}

class Keywords:
    def __init__(self, bot):
        self.bot = bot
        self.loadCommands()
    
    def initCon(self):
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
    
    def loadCommands(self):
        self.initCon()
        cur.execute("SELECT * FROM heartshaker.keywords;")
        resultList = cur.fetchall()
        global keywordList
        keywordList = {}
        for row in resultList:
            keywordList[row[0]] = row[1]

    @commands.command()
    async def refresh(self):
        self.loadCommands()
            

    @commands.command()
    async def set(self, word, *, value=None):
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

    @commands.command()
    async def view(self):
        viewList = "**Commands:** \n"
        for key, value in keywordList.items():
            viewList += "`" + str(key) + "` " + str(value) + "\n"
        await self.bot.say(viewList)
    
    @commands.command()
    async def remove(self, word):
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

    async def on_message(self, msg):
        if msg.content.startswith('//'):
            word = str(msg)
            print(word)
            if word in forbidden:
                await self.bot.send_message("Word is here") 
                await self.bot.process_commands(msg)
            else:
                re.sub('//','', word, 1)
                if (keywordList.get(word) is not None):
                    await self.bot.send_message(msg.channel, keywordList[word], tts=True)
        
def setup(bot):
    bot.add_cog(Keywords(bot))