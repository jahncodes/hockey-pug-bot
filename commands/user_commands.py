from discord.ext import commands
from main.modals import registerModal
from discord import app_commands, Interaction
from main import embeds
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
    
    @app_commands.command(name='register', description=f"Register to play {config.footer} PUGs by linking your Slapshot ID to Discord!")
    async def register(self, interaction):
        """
        IMPLEMENT ME
        """
        # Ensure command was sent in proper category
        category = interaction.channel.category
        if category and category.id != config.categoryID:
            return
        
        register_model = registerModal()
        await interaction.response.send_modal(register_model)
        response = await register_model.wait()
        
    @commands.command()
    async def register(self, ctx):
        """
        IMPLEMENT ME
        """
        await ctx.reply(embed=await embeds.notificationErrorEmbed(f'Please use **/register** to successfully sign up for {config.footer}.'))


async def setup(client:commands.bot) -> None:
    await client.add_cog(user_commands(client))
        
    
    

























