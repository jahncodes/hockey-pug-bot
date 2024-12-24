import aiosqlite
import configparse as config


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