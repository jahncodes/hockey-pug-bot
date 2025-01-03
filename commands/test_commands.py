import io
import discord
from discord.ext import commands
import plotly.graph_objects as plot
import configparse as config


class test_commands(commands.Cog):
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
    
    # REQUIRES KALEIDO
    @commands.command()
    async def test(self, ctx):
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        y = [1200, 1220, 1118, 1225, 1229, 1237, 1229, 1256, 1278, 1289, 1278, 1256, 1301, 1323, 1345, 1356, 1364, 1379, 1389, 1409]
        
        fig = plot.Figure(data=plot.Scatter(x=x, y=y, color='black', linestyle='-', mode='lines', name='Sample Line'))
        
        fig.update_layout(
            title='MMR Progression over Time (Games Played)',
            xaxis_title='Games Played',
            yaxis_title='MMR (Matchmaking Rating)'
        )
        
        
        
        # Create IMG in memory
        image_bytes = io.BytesIO()
        fig.write_image(image_bytes, format='PNG')
        image_bytes.seek(0)
        
        # Save Plot File
        await ctx.reply(file=discord.File(fp=image_bytes, filename='plot.png'))
        
        
async def setup(client:commands.bot) -> None:
    await client.add_cog(test_commands(client))