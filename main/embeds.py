from datetime import datetime
from zoneinfo import ZoneInfo
import configparse as config
from main.logger import *
import discord

"""
GENERAL EMBEDS
"""
async def notificationEmbed(message):
    """
    notificationSuccessEmbed takes in a message and formats it automatically.
    message: Takes in the message that we are trying to format in a discord embed.
    returns: (object) Formatted and styled queue embed.
    """
    try:
        # Generate Embed
        embed = discord.Embed(
            colour= config.embedTheme,
            description=f'{message}')
        return embed
    except Exception as e:
        errorLog(f'Failed to return Notification Embed successfully: {e}')
        
async def notificationSuccessEmbed(message):
    """
    notificationSuccessEmbed takes in a message and formats it automatically.
    message: Takes in the message that we are trying to format in a discord embed.
    returns: (object) Formatted and styled queue embed.
    """
    try:
        # Generate Embed
        embed = discord.Embed(
            colour= config.greenColor,
            description=f'{config.emojiSuccess} {message}')
        return embed
    except Exception as e:
        errorLog(f'Failed to return Success Notification Embed successfully: {e}')

async def notificationErrorEmbed(message):
    """
    notificationErrorEmbed takes in a message and formats it automatically as an error.
    message: Takes in the message that we are trying to format in a discord embed.
    returns: (object) Formatted and styled queue embed.
    """
    try:
        # Generate Embed
        embed = discord.Embed(
            colour= config.redColor,
            description=f'{config.emojiCancel} {message}')
        return embed
    except Exception as e:
        errorLog(f'Failed to return Error Notification Embed successfully: {e}')
    
"""
QUEUE EMBEDS
"""

async def queueEmbed(queue):
    """
    queueEmbed takes in the queue and returns a formatted and styled queue embed.
    queue: Takes in the queue that we are using to format the embed correctly.
    returns: (object) Formatted and styled queue embed.
    """
    try:
        # Generate Queue Template
        embed = discord.Embed(
            title=config.queueTitle,
            colour= config.embedTheme,
            description='')
        embed.set_thumbnail(url=f'{config.thumbnail}')
        # Dynamically generate queue
        for i in range(config.playerCount):
            #if len(queue) > i:
            #    embed.add_field(name=f'{config.arrowDownGreen} **Player {i + 1}** {config.arrowDownGreen}', value=f'᲼᲼᲼<@{str(queue[i])}>', inline=False)
            #else:
            #    embed.add_field(name=f'{config.arrowDownRed} __**Player {i + 1}**__ {config.arrowDownRed}', value='\u200b', inline=False)
            if len(queue) > i:
                embed.description += f"{config.emojiGreen}\u00A0\u00A0**Player {i + 1}:** <@{str(queue[i])}>\u00A0\u00A0\u00A0\u00A0\n\n\n"
            else:
                embed.description += f"{config.emojiRed}\u00A0\u00A0**Player {i + 1}:**\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\n\n\n"
        return embed
    except Exception as e:
        errorLog(f'Failed to return Queue Embed successfully: {e}')

async def queueNotiEmbed(discordID, action, color):
    """
    queueNotiEmbed takes in the queue and returns a formatted and styled queue embed.
    params:
        discordID: Takes in the discordID that we are using to format the embed correctly.
        action: The type of action happened (joined, left).a
        color: The color of the embed for the theme.
    returns: (object) Formatted and styled queue noti embed.
    """
    try:
        # Add respective emoji
        emoji = ''
        if (action == 'joined'):
            emoji = config.emojiSuccess
        elif (action == 'left'):
            emoji = config.emojiCancel
        
        # Generate notification embed
        embed = discord.Embed(
            description=f'{emoji} **<@{str(discordID)}> has {action} the Queue!**' if str(discordID) != '' else f'**Nobody has {action} the Queue!**', 
            color=color)
        
        # Get current time for embed and attach to footer ()
        #time = datetime.now(ZoneInfo('America/New_York'))
        #format = time.strftime('%I:%M %p')
        #embed.set_footer(text=config.footer + format, icon_url=config.footerIcon)
        embed.set_footer(text=f'{config.footer} | Time Here (Not Implemented)', icon_url=config.footerIcon)

        return embed
    except Exception as e:
        errorLog(f'Failed to return Queue Notification Embed successfully: {e}')

"""
DRAFT EMBEDS
"""

async def draftEmbed(playerDiscordID):
    """
    IMPLEMENT ME!
    """





"""
MATCH EMBEDS
"""



"""
STAT EMBEDS
"""
async def statEmbed(seasonNumber, userStatData, discordUser):
    title = discordUser.display_name + "'s"
    
    # Set Title (using number logic: 0 is false, any other number = True)
    embed = discord.Embed(colour=config.embedTheme)
    
    # Set Thumbnail
    if discordUser.avatar is None:
        embed.set_thumbnail(url=config.defaultPicture)
    else:
        embed.set_thumbnail(url=discordUser.avatar._url)
    
    if seasonNumber:
        title += f' Season {seasonNumber} Statistics'
        embed.title = title
        embed.add_field(name='MMR', value=userStatData[1], inline=True)
        embed.add_field(name="Score", value=userStatData[2], inline=True)
        embed.add_field(name="Goals", value=userStatData[3], inline=True)
        embed.add_field(name="Assists", value=userStatData[4], inline=True)
        embed.add_field(name="Points", value=userStatData[5], inline=True)
        embed.add_field(name="Shots", value=userStatData[6], inline=True)
        embed.add_field(name="Posts Hit", value=userStatData[7], inline=True)
        embed.add_field(name="Passes", value=userStatData[8], inline=True)
        embed.add_field(name="Saves", value=userStatData[9], inline=True)
        embed.add_field(name="Blocks", value=userStatData[10], inline=True)
        embed.add_field(name="Takeaways", value=userStatData[11], inline=True)
        embed.add_field(name="Turnovers", value=userStatData[12], inline=True)
        embed.add_field(name="Faceoffs Won", value=userStatData[13], inline=True)
        embed.add_field(name="Faceoffs Lost", value=userStatData[14], inline=True)
        embed.add_field(name="Possession", value=f'{userStatData[15]} seconds', inline=True)
        embed.add_field(name="Wins", value=userStatData[16], inline=True)
        embed.add_field(name="Losses", value=userStatData[17], inline=True)
        embed.add_field(name="Games Played", value=userStatData[18], inline=True)
    else:
        title += f' All-Time Profile'
        embed.title = title
        embed.add_field(name='Slap ID', value=userStatData[1], inline=True)
        embed.add_field(name='Peak MMR', value=userStatData[2], inline=True)
        embed.add_field(name='XP Points', value=userStatData[3], inline=True)
        embed.add_field(name="Score", value=userStatData[4], inline=True)
        embed.add_field(name="Goals", value=userStatData[5], inline=True)
        embed.add_field(name="Assists", value=userStatData[6], inline=True)
        embed.add_field(name="Points", value=userStatData[7], inline=True)
        embed.add_field(name="Shots", value=userStatData[8], inline=True)
        embed.add_field(name="Posts Hit", value=userStatData[9], inline=True)
        embed.add_field(name="Passes", value=userStatData[10], inline=True)
        embed.add_field(name="Saves", value=userStatData[11], inline=True)
        embed.add_field(name="Blocks", value=userStatData[12], inline=True)
        embed.add_field(name="Takeaways", value=userStatData[13], inline=True)
        embed.add_field(name="Turnovers", value=userStatData[14], inline=True)
        embed.add_field(name="Faceoffs Won", value=userStatData[15], inline=True)
        embed.add_field(name="Faceoffs Lost", value=userStatData[16], inline=True)
        embed.add_field(name="Possession", value=f'{userStatData[17]} seconds', inline=True)
        embed.add_field(name="+/-", value=f"{'+' + str(userStatData[21]) if userStatData[21] > 0 else ('-' + str(abs(userStatData[21]))) if userStatData[21] < 0 else userStatData[21]}", inline=True)
        embed.add_field(name="Wins", value=userStatData[18], inline=True)
        embed.add_field(name="Losses", value=userStatData[19], inline=True)
        embed.add_field(name="Games Played", value=userStatData[20], inline=True)
    
    embed.set_footer(text=f'{config.footer} | Player Statistics', icon_url=config.footerIcon)
    
    return embed