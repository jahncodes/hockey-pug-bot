import random
from discord.ui import Button, View
from systems.match import match
import aiosqlite
import discord
import configparse as config
import asyncio

class draft():
    global activeDraft
    activeDrafts = []
    
    def __init__(self, client, queue):
        self.client = client
        self.queue = queue
        
    async def startDraft(self, ids):
        print("IMPLEMENT ME")
    
    async def postDraftEmbed(self):
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
        print("IMPLEMENT ME")
        
    async def assignCaptains(self):
        print("IMPLEMENT ME")