from datetime import datetime
from zoneinfo import ZoneInfo
import configparse as config
from main.logger import *
import discord

async def queueEmbed(queue):
    '''
    queueEmbed takes in the queue and returns a formatted and styled queue embed.
    queue: Takes in the queue that we are using to format the embed correctly.
    returns: (object) Formatted and styled queue embed.
    '''
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
                embed.description += f"{config.emojiGreen}\u00A0\u00A0__**Player {i + 1}:**__ <@{str(queue[i])}>\u00A0\u00A0\u00A0\u00A0\n\n\n"
            else:
                embed.description += f"{config.emojiRed}\u00A0\u00A0__**Player {i + 1}:**__\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\n\n\n"
        return embed
    except Exception as e:
        errorLog(f'Failed to return Queue Embed successfully: {e}')

async def queueNotiEmbed(discordID, action, color):
    '''
    queueNotiEmbed takes in the queue and returns a formatted and styled queue embed.
    params:
        discordID: Takes in the discordID that we are using to format the embed correctly.
        action: The type of action happened (joined, left).a
        color: The color of the embed for the theme.
    returns: (object) Formatted and styled queue noti embed.
    '''
    try:
        # Add respective emoji
        emoji = ''
        if (action == 'joined'):
            emoji = config.emojiJoin
        elif (action == 'left'):
            emoji = config.emojiLeave
        
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
