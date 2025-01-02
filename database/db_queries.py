import aiosqlite
import configparse as config
from main import embeds


async def fetchPlayerAllTimeData(discordID):
    """
    fetchPlayerAllTimeData uses an sql query to fetch all-time data for a player using their discord ID.
    params:
        discordID: the discord ID of the player we want the all-time data for.
    returns: (tupile) containing all the listed statistics that connects with the discordID.
    """
    async with aiosqlite.connect(f'{config.dbName}.db') as db:
        # SQL query to fetch all the columns for the specified discordID
        sqlQuery = 'SELECT * FROM AllTimeData WHERE discordID = ?'
        # Execute query with params (discordID)
        async with db.execute(sqlQuery, (discordID,)) as cursor:
            # Fetch the first result (discordID is primary key so it is unique)
            result = await cursor.fetchone()
                
            # Return the result or None if entry does not exist
            return result
            
async def fetchPlayerSeasonData(discordID, seasonNumber):
    """
    fetchPlayerAllTimeData uses an sql query to fetch the specified season data for a player using their discord ID.
    params:
        discordID: the discord ID of the player we want the season data for.
        seasonNumber: The season number we want the statistics for.
    returns: (tupile) containing all the listed statistics that connects with the discordID in the specified season table.
    """
    async with aiosqlite.connect(f'{config.dbName}.db') as db:
        # SQL query to fetch all the columns for the specified discordID in the specified season table
        sqlQuery = f'SELECT * FROM season{seasonNumber}Data WHERE discordID = ?'
        # Execute query with params (discordID)
        async with db.execute(sqlQuery, (discordID,)) as cursor:
            # Fetch the first result (discordID is primary key so it is unique)
            result = await cursor.fetchone()
                
            # Return the result or None if entry does not exist
            return result
            
async def checkPlayerDiscordinDB(discordID):
    """
    checkPlayerinDB uses an sql query to check if the specified ID exists in the database.
    params:
        discordID: the discord ID of the user we are checking to see if they exist
    returns: (boolean) true if the user exists in the database, false if they don't exist
    """
    async with aiosqlite.connect(f'{config.dbName}.db') as db:
        # SQL query to check if the specified discordID is in our all-time data table
        sqlQuery = f'SELECT 1 FROM AllTimeData WHERE DiscordID = ? LIMIT 1'
        # Execute query with params (discordID)
        async with db.execute(sqlQuery, (discordID,)) as cursor:
            result = await cursor.fetchone()
                
            return result is not None
        
async def checkPlayerSlapinDB(slapID):
    """
    checkPlayerinDB uses an sql query to check if the specified ID exists in the database.
    params:
        slapID: the slap ID of the user we are checking to see if they exist
    returns: (boolean) true if the user exists in the database, false if they don't exist
    """
    async with aiosqlite.connect(f'{config.dbName}.db') as db:
        # SQL query to check if the specified discordID is in our all-time data table
        sqlQuery = f'SELECT 1 FROM AllTimeData WHERE SlapID = ? LIMIT 1'
        # Execute query with params (discordID)
        async with db.execute(sqlQuery, (slapID,)) as cursor:
            result = await cursor.fetchone()
                
            return result is not None
        
async def registerPlayerInDB(discordID, slapID):
    """
    registerPlayerInDB is not a query, but links discord user to in-game through IDs and creates entries into table as needed. 
    params:
        discordID: the discord ID of the user we are registering.
        slapID: the slapshot ID of the user we are registering.
    returns:
        (boolean) True: if the discordID/slapID was successfully added to the database. 
        (boolean) False: if the discordID/slapID is already in the database.
    """
    async with aiosqlite.connect(f'{config.dbName}.db') as db:
        # Ensure discordID and slapID is not in the database already.
        if (await checkPlayerDiscordinDB(discordID) and await checkPlayerSlapinDB(slapID)):
            return False
        
        print(f'Discord ID in DB: {await checkPlayerDiscordinDB(discordID)}')
        print(f'Slap ID in DB: {await checkPlayerSlapinDB(slapID)}')
        
        # Add User to DB
        sqlAllTimeEntry = (f'INSERT INTO AllTimeData (DiscordID, SlapID) VALUES (?, ?)')
        allTimeValues = (discordID, slapID)   
        try:
            # Execute All-Time Data Table entry
            await db.execute(sqlAllTimeEntry, allTimeValues)
            
            # Execute Season Data Table(s) entry
            for i in range(1, config.activeSeason + 1):
                sqlSeasonEntry = (f'INSERT INTO season{i}Data (DiscordID) VALUES (?)')
                seasonValues = ((discordID,))
                
                await db.execute(sqlSeasonEntry, seasonValues)
            
            await db.commit()
            print("Player added to DB!")
            return True
        except Exception as e:
            await embeds.notificationErrorEmbed(f'Failed to add player to the database: {e}')
            return False
            
            
    