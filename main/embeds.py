from datetime import datetime
from zoneinfo import ZoneInfo
import configparse as config
import discord

async def queueEmbed(queue):
    '''
    queueEmbed takes in the queue and returns a formatted and styled queue embed.
    queue: Takes in the queue that we are using to format the embed correctly.
    returns: (object)cFormatted and styled queue embed.
    '''
    # Generate Queue Template
    embed = discord.Embed(
        title=config.queueTitle,
        description='',
        colour=int(config.embedTheme, 16))
    embed.set_thumbnail(url=f'{config.thumbnail}')

    # Dynamically generate queue
    for i in range(config.playerCount):
        player = f'<@{str(queue[i])}>' if len(queue) > i else ''
        embed.add_field(name=f'**Player {i + 1}:**', value=player, inline=False)

    return embed

async def queueNotiEmbed(discordID, action, color):
    '''
    queueNotiEmbed takes in the queue and returns a formatted and styled queue embed.
    discordID: Takes in the discordID that we are using to format the embed correctly.
    action: The type of action happened (joined, left).a
    color: The color of the embed for the theme.
    returns: (object) Formatted and styled queue noti embed.
    '''
    # Generate notification embed
    embed = discord.Embed(
        description=f'<@{str(discordID)}> has {action} the Queue!' if str(discordID) != '' else f'**Nobody has {action} the Queue!', 
        color=color)
    
    # Get current time for embed and attach to footer
    time = datetime.now(ZoneInfo('America/New_York'))
    format = time.strftime('%I:%M %p')
    embed.set_footer(text=config.footer + format, icon_url=config.footerIcon)

    return embed
