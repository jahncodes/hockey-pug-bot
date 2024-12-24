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
        '''
        allTimeDataDBSetup initializes the all-time data table that tracks a player statistics.
        '''
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
        '''
        allTimeDataDBSetup initializes the neccessary season(s) data tables that track player statistics.
        '''
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
    
    async def fetchPlayerAllTimeData(self, discordID):
        '''
        fetchPlayerAllTimeData uses an sql query to fetch all-time data for a player using their discord ID.
        discordID: the discord ID of the player we want the all-time data for.
        returns: (tupile) containing all the listed statistics that connects with the discordID.
        '''
        async with aiosqlite.connect(config.dbName) as db:
            # SQL query to fetch all the columns for the specified discordID
            sqlQuery = 'SELECT * FROM AllTimeData WHERE discordID = ?'
            # Execute query with params (discordID)
            async with db.execute(sqlQuery, (discordID,)) as cursor:
                # Fetch the first result (discordID is primary key so it is unique)
                result = await cursor.fetchone()
                
                # Commit changes and close connections (I believe happens automatically anyways with async but to be safe)
                await db.commit()
                await cursor.close()
                await db.close()
                
                # Return the result or None if entry does not exist
                return result
            
    async def fetchPlayerSeasonData(self, discordID, season):
        '''
        fetchPlayerAllTimeData uses an sql query to fetch the specified season data for a player using their discord ID.
        discordID: the discord ID of the player we want the season data for.
        season: The season we want the statistics for.
        returns: (tupile) containing all the listed statistics that connects with the discordID in the specified season table.
        '''
        async with aiosqlite.connect(config.dbName) as db:
            # SQL query to fetch all the columns for the spciefied discordID in the specified season table
            sqlQuery = f'SELECT * FROM season{season}Data WHERE discordID = ?'
            # Execute query with params (discordID)
            async with db.execute(sqlQuery, (discordID,)) as cursor:
                # Fetch the first result (discordID is primary key so it is unique)
                result = await cursor.fetchone()
                
                # Commit changes and close connections (I believe happens automatically anyways with async but to be safe)
                await db.commit()
                await cursor.close()
                await db.close()
                
                # Return the result or None if entry does not exist
                return result
            
    async def checkPlayerinDB(self, discordID):
        '''
        checkPlayerinDB uses an sql query to check if the specified ID exists in the database.
        discordID: the discord ID of the user we are checking to see if they exist
        returns: (boolean) true if the user exists in the database, false if they don't exist
        '''
        async with aiosqlite.connect(config.dbName) as db:
            # SQL query to check if the specified discordID is in our all-time data table
            sqlQuery = f'SELECT 1 FROM AllTimeData WHERE DiscordID = ? LIMIT 1'
            # Execute query with params (discordID)
            async with db.execute(sqlQuery, (discordID,)) as cursor:
                result = await cursor.fetchone()

                # Commit changes and close connections (I believe happens automatically anyways with async but to be safe)
                await db.commit()
                await cursor.close()
                await db.close()
                
                return result is not None
            
async def setup(client:commands.bot) -> None:
    await client.add_cog(database(client))