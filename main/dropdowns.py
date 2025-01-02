import discord
import configparse as config
from database import db_queries
from main import embeds

class profileDropdown(discord.ui.Select):
    def __init__(self, ctx, message, member):
        self.ctx = ctx
        self.message = message
        self.member = member
        options = [discord.SelectOption(label='All-Time Profile', description='View cumulative statistics from across all PUG seasons.')]
        
        # Dynamically Add Past Season Dropdowns
        for i in range(1, config.activeSeason):
            options.append(discord.SelectOption(label=f'Season {i} Statistics', description=f'View statistics from Season {i} PUGs.'))
        # Add Active Season Dropdown
        options.append(discord.SelectOption(label=f'Season {config.activeSeason} Statistics', description=f'View statistics from Season {config.activeSeason} PUGs.'))
        super().__init__(placeholder='Choose an option...', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction):
        userData = None
        seasonNumber = None
        
        # 1: Ensure Interaction is from Author of Message
        if interaction.user != self.ctx.author:
            await interaction.response.defer()
            return
        
        # 2: Set Requested Params
        if self.values[0] == 'All-Time Profile':
            await interaction.response.defer()
            userData = await db_queries.fetchPlayerAllTimeData(interaction.user.id)
            seasonNumber = 0
        else:
            # Extract Season Number
            if 'Season' in self.values[0]:
                seasonNumber = self.values[0].split(' ')[1]
                await interaction.response.defer()
                userData = await db_queries.fetchPlayerSeasonData(interaction.user.id, seasonNumber)
                
        # 3: Edit Message
        await self.message.edit(embed=await embeds.statEmbed(seasonNumber, userData, self.member))
        
class profileDropdownView(discord.ui.View):
    def __init__(self, ctx, message, member, timeout=300):
        super().__init__()
        self.add_item(profileDropdown(ctx, message, member))

        
        
        