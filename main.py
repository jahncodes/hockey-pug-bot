from main.systems.queue import queue
#from main.systems.match import match
from discord.ext import commands
from main.logger import *
import configparse as config
import platform
import discord

# Custom discord bot class inheriting from commands.Bot.
class Client(commands.Bot):
    def __init__(self):
        """
        __init__ initializes the class (bot) with a custom command prefix and intents for neccessary events.
        """
        super().__init__(command_prefix=commands.when_mentioned_or(config.prefix), intents=discord.Intents().all())
        self.activeLB = None
        self.cogslist = [
            "database.db",
        ]
    
    async def setup_hook(self):
        """
        setup_hook sets up the bot before it connects to Discord services as well as loads all the extensions (cogs) listed in self.cogslist.
        """
        for ext in self.cogslist:
            await self.load_extension(ext)
            
    async def on_ready(self):
        """
        on_ready prints bot information, clears channel history where old embeds may be, initializes systems, and sets the bot's activity presence.
        """
        
        # Print information to the console when the bot is ready to ensure correct versions and log-in.
        warningLog("Ensure information below is accurate before continuing.")
        infoLog(f"Logged in as:", f"{self.user.name}")
        infoLog(f"Discord Version:", f"{discord.__version__}")
        infoLog(f"Python Version:", str(platform.python_version()))
        infoLog(f"Hockey PUG Bot Version 2.0 by:", "John")
        await self.tree.sync()
        await self.wait_until_ready()
        
        # Clear channel history where old embeds may be
        async for message in self.get_channel(config.queueChannelID).history(limit=2):
            await message.delete()
        async for message in self.get_channel(config.lbChannelID).history(limit=1):
            await message.delete()
        
        # Initializes queue system.
        queue(Client)
        
        # Generate a match instance, launch leaderboard, and clean up class afterward. 
        #matchInstance = match(self, None, None, None, None, None)
        #await matchInstance.lb()
        #del matchInstance
        
        # Set the bot's presence to initial activity.
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over 0 PUG matches!"))

# Intitiate the bot client.
client = Client()

# Run the bot using discord token from configuration file. 
client.run(config.token)
