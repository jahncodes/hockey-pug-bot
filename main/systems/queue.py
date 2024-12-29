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
    """
    Represents a queue with it's respective properties and customization.
    
    This class models a queue system on discord using embeds where players can join and leave, with features such as inactivity, and notification checks automatically.
    
    Attributes:
        client (object): The discord bot client.
    
    Methods:
        postQueueEmbed(discordID, action, color): posts the queue and notification embed along with buttons needed for the system.
        createButtons(): generates the discord buttons such as 'Join' and 'Leave' so players can communicate with the class.
        joinCallback(interaction): a callback function for the Join button.
        leaveCallback(interaction): a callback function for the Leave button.
        addPlayerToQueue(discordID): adds a specified player to queue.
        removePlayerFromQueue(discordID): removes a specified player from queue.
        beginDraft(): creates a draft class instance.
        checkIfPlayerInQueue(discordID): checks if a specified player is in the queue.
        checkIfPlayerInMatch(discordID): checks if a specified player is in an active match.
        checkIfCooldownActive(discordID): checks if a button cooldown is active for a specified player.
        checkForInactivity(): checks if the queue has been active for a specified amount of time and performs tasks if it is.
        notifyAllPlayers(): checks if the queue has been filled 66% or more, and notifies all players to join the queue if so.
        
    """
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
            successLog('Asyncio Task Cancelled.')

    async def postQueueEmbed(self, discordID, action, color):
        """
        postQueueEmbed utilizes our embeds.py module to generate a queue embed or update the previous one if one exists already.
        params:
            discordID: the discord ID of the user you are trying to display has 'joined' or 'left' the queue.
            action: the action that the ID committed such as 'joined' or 'left' the queue to display in the notification embed.
            color: the color of the notification embed. 
        returns:
            (int) 1 if the player has an active cooldown and does not add them to queue.
            (int) 2 if the player is not registered and does not add them to queue.
            (int) 3 if the player is not in the queue and does not add them to queue.
            (int) 4 if the player was successfully added to the queue.
        """
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
        """
        createButtons generates the discord buttons we will use so we can track players who join and leave the queue.
        """
        joinButton = Button(label="Join", style=discord.ButtonStyle.green)
        leaveButton = Button(label="Leave", style=discord.ButtonStyle.danger)
        joinButton.callback = self.joinCallback
        leaveButton.callback = self.leaveCallback
        self.view.add_item(joinButton)
        self.view.add_item(leaveButton)

    async def joinCallback(self, interaction):
        """
        joinCallback is a callback function for the join button that specifies how we handle a button click.
        params:
            interaction: The interaction from the user clicking our button.
        """
        try:
            discordID = interaction.user.id
            
            # Check if Queue is already full.
            if len(self.queue) >= config.playerCount:
                await interaction.response.send_message('✖ A match is already starting!', ephemeral=True)
                return
            
            result = await self.addPlayerToQueue(discordID)
                
            if (result == 1):
                # Case 1: Player has Active Cooldown
                await interaction.response.send_message(f"✖ You have an active cooldown of {round(max(0, self.cooldowns[discordID] - time.time()), 1)} seconds!", ephemeral=True)
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
        """
        leaveCallback is a callback function for the leave button that specifies how we handle a button click.
        params:
            interaction: The interaction from the user clicking our button.
        """
        try:
            discordID = interaction.user.id
            
            # Check if Queue is already full.
            if len(self.queue) >= config.playerCount:
                await interaction.response.send_message('✖ A match is already starting!', ephemeral=True)
                return
            
            result = await self.removePlayerFromQueue(discordID)
            
            if (result == 1):
                # Case 1: Player has Active Cooldown
                await interaction.response.send_message(f"✖ You have an active cooldown of {round(max(0, self.cooldowns[discordID] - time.time()), 1)} seconds!", ephemeral=True)
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
            errorLog(f"Failed to remove Player from Queue: {e}")
            if not self.checkIfBeginDraft:
                if len(self.queue) >= config.playerCount:
                    await self.beginDraft()
                    return

    async def addPlayerToQueue(self, discordID):
        """
        addPlayerToQueue performs various checks and if passed, will successfully add the player to the Queue.
        params:
            discordID: the discord ID of the user you are trying to add to the queue.
        returns:
            (int) 1 if the player has an active cooldown and does not add them to queue.
            (int) 2 if the player is not registered and does not add them to queue.
            (int) 3 if the player is not in the queue and does not add them to queue.
            (int) 4 if the player was successfully added to the queue.
        """
        # 1: Player has Active Cooldown
        if (await self.checkIfCooldownActive(discordID)):
            return 1
        # 2: Player is already in the Queue
        elif (await self.checkIfPlayerInQueue(discordID)):
            return 2
        # 3: Player is not Registered
        elif (not await db_queries.checkPlayerinDB(self, discordID)):
            return 3
        # 4: Player is in an Active Match already
        elif (await self.checkIfPlayerInMatch(discordID)):
            return 4
        # 5: Add Player to Queue and Check if Full
        else:
            self.queue.append(discordID)
            await self.postQueueEmbed(discordID, "joined", 0x90EE90)
            successLog(f'Discord ID: {discordID} has been added to the queue.')
            return 5
            
    async def removePlayerFromQueue(self, discordID):
        """
        removePlayerFromQueue performs various checks and if passed, will successfully remove the player from the Queue.
        params:
            discordID: the discord ID of the user you are trying to remove from the queue.
        returns:
            (int): 1 if the player has an active cooldown and does not remove them from queue.
            (int): 2 if the player is not registered and does not remove them from queue.
            (int): 3 if the player is not in the queue and does not remove them from queue.
            (int): 4 if the player was successfully removed from the queue.
        """
        # 1: Player has Active Cooldown
        if (await self.checkIfCooldownActive(discordID)):
            return 1
        # 2: Player is not Registered
        elif (not await db_queries.checkPlayerinDB(self, discordID)):
            return 2
        # 3: Player is not in the Queue
        elif (not await self.checkIfPlayerInQueue(discordID)):
            return 3
        # 4: Remove Player from Queue
        else:
            self.queue.remove(discordID)
            await self.postQueueEmbed(discordID, "left", 0xd83c3e)
            successLog(f'Discord ID: {discordID} has been removed from the queue.')
            return 4
            
    async def beginDraft(self, discordID):
        """
        IMPLEMENT ME!!!!
        """
        return False
        
    async def checkIfPlayerInQueue(self, discordID):
        """
        checkIfPlayerInQueue
        
        returns: (boolean) True if the discordID is found in the queue, otherwise returns False.
        """    
        for i in self.queue:
            if (i == discordID):
                return True
        return False
        
    async def checkIfPlayerInMatch(self, discordID):
        """
        IMPLEMENT ME!!!!
        """
        return False
    
    async def checkIfCooldownActive(self, discordID):
        """
        checkIfCooldownActive will go in the cooldown dictionary and see if a player has an active cooldown and return the discordID if found.
        
        returns: (int) of the discordID if found in the dictionary, otherwise None.
        """    
        return discordID in self.cooldowns and self.cooldowns[discordID] > time.time()
        
    async def checkForInactivity(self):
        """
        checkForInactivity will sleep for config.queueInactivity time and check if any action has happened since then, and clear the queue and perform other actions if so.
        """    
        while not self.checkIfBeginDraft:
            try:
                await asyncio.sleep(config.queueInactivity)
            except asyncio.CancelledError:
                successLog('Asyncio Task Cancelled.')
            
            currentTime = time.time()
            
            if self.clicked and ((currentTime - self.clicked) > config.queueInactivity):
                # 1: Queue is Empty
                if (len(self.queue) == 0):
                    return
                elif (len(self.queue) == 6):
                    return
                else:
                    for i in self.queue:
                        user = await self.client.fetch_user(i)
                        
                        try:
                            await user.send(f"THe queue has been idle for more than {int(config.queueInactivity / 60)} minutes, thus you have been automatically removed from it. Feel free to join again!")
                        except Exception as e:
                            await self.client.get_channel(config.discussionChannelID).send(f"<@{i}> THe queue has been idle for more than {int(config.queueInactivity / 60)} minutes, thus you have been automatically removed from it. Feel free to join again!")
                            errorLog(f'Failed to send Player DM when notifying of queue inactivity. Using alternative method to send notification in server: {e}')
                    self.queue.clear()
                    await self.postQueueEmbed("", "joined", 0xfff47c)
                    self.clicked = None
                    successLog(f'Queue has been cleared due to inactivity after {int(config.queueInactivity / 60)} minutes.')
        
    async def notifyAllPlayers(self):
        """
        notifyAllPlayers will sleep for specified config time when queue hits 66% full or more and then will check if it is still 4/6 or >, and if so notify all players with a specified role to join the queue.
        """    
        # A notification to join Queue is already on-going
        if self.activeNoti:
            return
        self.activeNoti = True
            
        try:
            await asyncio.sleep(config.queueNotification)
        except asyncio.CancelledError:
            successLog('Asyncio Task Cancelled.')
            
        # 1: Queue threshold is not reached yet!
        if (len(self.queue) < 4 or (len(self.queue) >= 6)):
            return
        # 2: Notify players!
        else:
            await self.client.get_channel(config.discussionChannelID).send(f"<@&{config.notificationRoleID}> {len(self.queue)}/6 players in Queue! Get pugging!")
            self.activeNoti = False
            
            
            
                
        
    