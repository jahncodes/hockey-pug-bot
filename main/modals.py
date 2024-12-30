from discord.ui import Modal, TextInput
import configparse as config
import discord

class registerModal(Modal, title=f'{config.footer} Register Form'):
    info = TextInput(
        label="How to find Slap ID!", 
        placeholder="Slapshot ID can be found under 'Player' tab in-game, and clicking 'identity.' You should see the ID as a number in small white text at the top of the UI.",
        required=False)
    game_id = TextInput(label='Slapshot ID', placeholder='Example: 429195', style=discord.TextStyle.short)
    
    def __init(self):
        super().__init__()
        self.gameID = None
        self.on_submit_interaction = None
    
    async def on_submit(self, interaction):
        self.gameID = self.game_id.value
        self.on_submit_interaction = interaction
        self.stop()