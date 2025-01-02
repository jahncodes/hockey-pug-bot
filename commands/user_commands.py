import discord
from discord.ext import commands
from main.modals import registerModal
from discord import app_commands, Interaction
from database import db_queries
from main import embeds
from main import dropdowns
import asyncio
import configparse as config

class user_commands(commands.Cog):
    """
    Represents all possible user commands in a Cog to allow live reloading without restarting bot.
    
    This class models all possible user commands in a Cog that the bot listens to.
    
    Attributes:
        client (object): The discord bot client.
    
    Methods:
        register(discordID, interaction): Registers a player in the database, and links their in-game ID to discord ID using the register modal.
        
    """
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name='register', description=f"Register to play {config.footer} by linking your Slapshot ID to Discord!")
    @app_commands.guild_only()
    async def register(self, interaction):
        """
        IMPLEMENT ME
        """
        # 1: Ensure command was sent in proper category
        category = interaction.channel.category
        if category and category.id != config.categoryID:
            await interaction.response.send_message(embed=await embeds.notificationErrorEmbed(f'You can\'t register in this category!'), ephemeral=True)
            return
        
        register_model = registerModal()
        await interaction.response.send_modal(register_model)
        response = await register_model.wait()
        
        # 2: Parameter is an Integer
        if not await self.isInteger(register_model.gameID):
            await register_model.on_submit_interaction.response.send_message(embed=await embeds.notificationErrorEmbed(f'{register_model.gameID} is not a valid Slapshot ID! Try again.'), ephemeral=True)
            return
        
        result = await db_queries.registerPlayerInDB(interaction.user.id, int(register_model.gameID))
        print(result)
        
        if (result == True):
            await register_model.on_submit_interaction.response.send_message(embed=await embeds.notificationSuccessEmbed(f'You have successfully registered for {config.footer} with the **Slapshot ID: {register_model.gameID}!**'), ephemeral=True)
        elif (result == False):
            await register_model.on_submit_interaction.response.send_message(embed=await embeds.notificationErrorEmbed(f'This **Discord User** or **Slapshot ID** provided is already linked to a profile! Contact an administrator if you think this is incorrect.'), ephemeral=True)
    
    async def isInteger(self, text):
        flag = True
        try:
            int(text)
        except:
            flag = False
        return flag
    
    @commands.command()
    async def stats(self, ctx, member:discord.Member = None):
        """
        IMPLEMENT ME
        """
        # 1: Check if a member was given as argument
        member = member or ctx.author
        
        # 2: Verify Message is in Correct Category
        category = ctx.channel.category
        if category and category.id != config.categoryID:
            return
        
        # 3: Generate Active Season Embed as Default Option and Check if User Exists
        userData = await db_queries.fetchPlayerSeasonData(member.id, config.activeSeason)
        if userData is None:
            await ctx.reply(embed=await embeds.notificationErrorEmbed('The user provided is not registered so there are no stats to display.'))
            return
            
        embed = await embeds.statEmbed(config.activeSeason, userData, member)
        
        # 5: Generate Dropdown and send embed
        view = dropdowns.profileDropdownView(ctx, None, member)
        view.children[0].message = await ctx.reply(embed=embed, view=view)
        
async def setup(client:commands.bot) -> None:
    await client.add_cog(user_commands(client))
        
    
    

























