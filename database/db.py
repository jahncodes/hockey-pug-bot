from discord.ext import commands
import aiosqlite
import asyncio
import configparse as config

class database(commands.Cog):
    def __init__(self, client):
        self.client = client
        asyncio.create_task(self.allTimeDataDBSetup())
        asyncio.create_task(self.seasonsDataDBSetup())
        
    async def allTimeDataDBSetup(self):
        """
        allTimeDataDBSetup initializes the all-time data table that tracks a player statistics.
        """
        async with aiosqlite.connect(f'{config.dbName}.db') as db:
            # Initializes All-Time Data table if it does not exist on start-up.
            sqlQuery = f'''CREATE TABLE IF NOT EXISTS AllTimeData (
                    DiscordID INT PRIMARY KEY,
                    SlapID INT,
                    SkillRating INT DEFAULT {config.startingSkillRating},
                    Score INT DEFAULT 0,
                    Goals INT DEFAULT 0,
                    Assists INT DEFAULT 0,
                    Shots INT DEFAULT 0,
                    PostHits INT DEFAULT 0,
                    Passes INT DEFAULT 0,
                    Saves INT DEFAULT 0,
                    Blocks INT DEFAULT 0,
                    Takeaways INT DEFAULT 0,
                    Turnovers INT DEFAULT 0,
                    FoWon INT DEFAULT 0,
                    FoLost INT DEFAULT 0,
                    Possession INT DEFAULT 0,
                    Wins INT DEFAULT 0,
                    Losses INT DEFAULT 0,
                    Gp INT DEFAULT 0,
                    Streak INT DEFAULT 0,
                    Points INT DEFAULT 0,
                    PlusMinus INT DEFAULT 0,
                    Xp INT DEFAULT 0)'''
                    
            await db.execute(sqlQuery)
        
    async def seasonsDataDBSetup(self):
        """
        allTimeDataDBSetup initializes the neccessary season(s) data tables that track player statistics.
        """
        async with aiosqlite.connect(f'{config.dbName}.db') as db: 
            # Initializes Season(s) Data table(s) if it does not exist on start-up.
            for x in range(1, config.activeSeason + 1):
                sqlQuery = f'''CREATE TABLE IF NOT EXISTS season{x}Data (
                        DiscordID INT PRIMARY KEY,
                        Score INT DEFAULT 0,
                        Goals INT DEFAULT 0,
                        Assists INT DEFAULT 0,
                        Shots INT DEFAULT 0,
                        PostHits INT DEFAULT 0,
                        Passes INT DEFAULT 0,
                        Saves INT DEFAULT 0,
                        Blocks INT DEFAULT 0,
                        Takeaways INT DEFAULT 0,
                        Turnovers INT DEFAULT 0,
                        FoWon INT DEFAULT 0,
                        FoLost INT DEFAULT 0,
                        Possession INT DEFAULT 0,
                        Wins INT DEFAULT 0,
                        Losses INT DEFAULT 0,
                        Gp INT DEFAULT 0,
                        Streak INT DEFAULT 0,
                        Points INT DEFAULT 0,
                        PlusMinus INT DEFAULT 0,
                        Xp INT DEFAULT 0,
                        FOREIGN KEY (DiscordID) REFERENCES AllTimeData(DiscordID) ON DELETE CASCADE)'''
                
                await db.execute(sqlQuery)
            
async def setup(client:commands.bot) -> None:
    await client.add_cog(database(client))