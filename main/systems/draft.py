import random
from discord.ui import Button, View
from systems.match import match
import aiosqlite
import discord
import configparse as config
from database import db_queries
import asyncio

class draft():
    global activeDraft
    activeDrafts = []
    
    def __init__(self, client, queue):
        self.client = client
        self.queue = queue
        self.playerSeasonData = {}
        self.homeTeamDiscordIDs = []
        self.awayTeamDiscordIDs = []
        self.draftBoardDiscordIDs = []
        self.activePick = 0
        
    async def startDraft(self):
        # 1: Ensure we have correct amount of players
        if len(self.queue) != config.playerCount:
            # Send back to queue class
            print('Implement Me')
    
        # 2: Extract Player Data from the Database and store in class
        await self.parsePlayerData()
        
        # 3: Generate a PUG ID for the Match
        print('Implement Me')
        
        # 4: Start Draft
        await self.postDraftEmbed(None)
    
    async def postDraftEmbed(self, discordID):
        print("IMPLEMENT ME")
        
    async def createButtons(self):
        print("IMPLEMENT ME")
        
    async def playerButtonClickedCallback(self):
        print("IMPLEMENT ME")
        
    async def addPlayerToTeam(self, discordID):
        print("IMPLEMENT ME")
        
    async def sendCaptainDM(self):
        print("IMPLEMENT ME")
        
    async def cancelDraftIfAFK(self):
        print("IMPLEMENT ME")
        
    async def cancelDraft(self):
        print("IMPLEMENT ME")
        
    async def parsePlayerData(self):
        # 1: Gather Player Data and Store in Dictionary
        for i in range(0, config.playerCount):
            playerDiscordID = self.queue[i]
            playerSeasonData = await db_queries.fetchPlayerSeasonData(playerDiscordID, config.activeSeason)
            self.playerSeasonData[playerDiscordID] = playerSeasonData
        
        # 2: Sort Data in Ascending Order
        self.playerSeasonData = sorted(self.playerSeasonData.values(), key=lambda x: x['MMR'], reverse=True)
        
    async def assignCaptains(self):
        # 1: Randomize Top Half of Players for Captain Selection
        numTopHalfPlayers = (config.playerCount // 2) - 1
        randomHomeNum = random.randint(0, numTopHalfPlayers)
        randomAwayNum = random.randint(0, numTopHalfPlayers)
        
        while randomHomeNum == randomAwayNum:
            randomAwayNum = random.randint(0, numTopHalfPlayers)
            
        # 2: Assign Captains to Respective Teams
        self.homeTeamDiscordIDs[0] = self.playerSeasonData[randomHomeNum]['DiscordID']
        self.awayTeamDiscordIDs[0] = self.playerSeasonData[randomAwayNum]['DiscordID']
        
        