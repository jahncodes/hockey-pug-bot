import asyncio
import time
from discord.ui import Button, View
from collections import deque
from main.logger import *
import configparse as config
import discord
from main import embeds
from database import db_queries

class queue():
    # Global variable to track the active queue.
    global activeQueue
    activeQueue = None

    def __init__(self, client):
        self.client = client
        # Set global variable to this object.
        global activeQueue
        activeQueue = self
        # Initialize deque.
        self.queue = deque()
        # Embeds
        self.queueEmbed = None
        self.notiEmbed = None
        # Etc
        self.cooldowns = {}
        self.cancelledTasks = []
        self.clicked = None
        self.checkIfBeginDraft = False
        self.activeNoti = False
        self.view = View(timeout=None)
        # On Class initialization
        try:
            self.cancelledTasks.append(asyncio.create_task(self.createButtons()))
            self.cancelledTasks.append(asyncio.create_task(self.postQueueEmbed('', 'joined', 0xfff47c)))
        except asyncio.CancelledError:
            warningLog('Task cancelled.')

    async def postQueueEmbed(self, discordID, action, color):
        try:
            if self.queueEmbed != None:
                await self.queueEmbed.edit(embed=await embeds.queueEmbed(self.queue))
                await self.notiEmbed.edit(embed=await embeds.queueNotiEmbed(discordID, action, color))
                successLog('Queue Embed updated!')
            else:
                self.queueEmbed = await self.client.get_channel(config.queueChannelID).send(embed=await embeds.queueEmbed(self.queue))
                self.notiEmbed = await self.client.get_channel(config.queueChannelID).send(embed=await embeds.queueNotiEmbed(discordID, action, color), view=self.view)
                successLog('Queue Embed posted!')
        except Exception as e:
            errorLog(f"Failed to post Queue Embed: {e}")
        
    async def createButtons(self):
        joinButton = Button(label="Join", style=discord.ButtonStyle.green)
        leaveButton = Button(label="Leave", style=discord.ButtonStyle.danger)
        joinButton.callback = self.joinCallback
        leaveButton.callback = self.leaveCallback
        self.view.add_item(joinButton)
        self.view.add_item(leaveButton)

        
    async def joinCallback(self, interaction):
        try:
            discordID = interaction.user.id
            
            # Check if Queue is already full.
            if len(self.queue) >= config.playerCount:
                await interaction.response.send_message('✖ A match is already starting!', ephemeral=True)
                return
            
            result = await self.addPlayerToQueue(discordID)
                
            if (result == 1):
                # Case 1: Player has Active Cooldown
                await interaction.response.send_message(f"✖ You have an active cooldown of {round(max(0, self.cooldowns[id] - time.time()), 1)} seconds!", ephemeral=True)
            elif (result == 2):
                # Case 2: Player is Already in Queue
                await interaction.response.send_message("✖ You are already in the Queue.", ephemeral=True)
            elif (result == 3):
                # Case 3: Player is not Registered
                await interaction.response.send_message("✖ You are not registered.", ephemeral=True)
            elif (result == 4):
                # Case 4: Player is in Active Match
                await interaction.response.send_message("✖ You are already in an active match! If the game just ended, please wait for the results to be processed.", ephemeral=True)
            else:
                # Case 5: Player has been added to Queue
                await interaction.response.defer()
                if (len(self.queue) >= config.playerCount):
                    # Create Draft
                    await self.beginDraft()
                elif (len(self.queue) >= (config.playerCount - 2)):
                    # Begin Async Notification Function
                    self.cancelledTasks.append(await self.notifyAllPlayers())
                # Apply Cooldown
                self.cooldowns[discordID] = time.time()
                self.clicked = time.time()
                if self.cancelledTasks:
                    self.cancelledTasks.append(await self.checkForInactivity())
        except discord.errors.NotFound:
            # Handle error accordingly by checking if queue is still full and continue to draft, otherwise no action
            errorLog('Discord Not Found Error when adding a player to the Queue.')
            if not self.beginDraft and (len(self.queue) >= config.playerCount):
                await self.beginDraft()
                return
    
    async def leaveCallback(self, interaction):
        try:
            discordID = interaction.user.id
            
            # Check if Queue is already full.
            if len(self.queue) >= config.playerCount:
                await interaction.response.send_message('✖ A match is already starting!', ephemeral=True)
                return
            
            result = await self.removePlayerFromQueue(discordID)
            
            if (result == 1):
                # Case 1: Player has Active Cooldown
                await interaction.response.send_message(f"✖ You have an active cooldown of {round(max(0, self.cooldowns[id] - time.time()), 1)} seconds!", ephemeral=True)
            elif (result == 2):
                # Case 2: Player is not Registered
                await interaction.response.send_message("✖ You are not registered.", ephemeral=True)
            elif (result == 3):
                # Case 3: Player is not in Queue
                await interaction.response.send_message("✖ You are not in the Queue.", ephemeral=True)
            else:
                # Case 4: Remove Player from Queue
                await interaction.response.defer()
                if (len(self.queue) != 0):
                    self.clicked = time.time()
                self.cooldowns[discordID] = time.time() + config.buttonCooldown
        except Exception as e:
            # Handle error accordingly by checking if queue is still full and continue to draft, otherwise no action
            errorLog(f"Failed to remove Player to Queue: {e}")
            if not self.beginDraft:
                if len(self.queue) >= config.playerCount:
                    await self.beginDraft()
                    return

    async def addPlayerToQueue(self, discordID):
        # 1: Player has Active Cooldown
        if await self.checkIfCooldownActive(discordID):
            return 1
        # 2: Player is already in the Queue
        if await self.checkIfPlayerInQueue(discordID):
            return 2
        # 3: Player is not Registered
        if not await db_queries.checkPlayerinDB(self, discordID):
            return 3
        # 4: Player is in an Active Match already
        if await self.checkIfPlayerInMatch(discordID):
            return 4
        # 5: Add Player to Queue and Check if Full
        self.queue.append(discordID)
        await self.postQueueEmbed(discordID, "joined", 0x90EE90)
        successLog(f'Discord ID {discordID} has been added to the queue.')
        return 5
            
    async def removePlayerFromQueue(self, discordID):
        print("Implement Me")
    
    async def beginDraft(self, discordID):
        print("Implement Me")
        
    async def checkIfPlayerInQueue(self, discordID):
        return False
        
    async def checkIfPlayerInMatch(self, discordID):
        return False
    
    async def checkIfCooldownActive(self, discordID):    
        return False
        
    async def checkForInactivity(self):
        print("Implement Me")
        
    async def notifyAllPlayers(self):
        print("Implement Me")
        
    