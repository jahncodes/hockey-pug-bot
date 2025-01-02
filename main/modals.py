from discord.ui import Modal, TextInput
import configparse as config
import discord

class registerModal(Modal, title=f'{config.footer} Register Form'):
    info = TextInput(
        label="How to find Slap ID! (NO ANSWER REQUIRED)", 
        placeholder="Found in-game through Player -> Identity -> Top of UI.",
        required=False)
    game_id = TextInput(label='Could you provide your Slapshot ID?', placeholder='Example: 429195', style=discord.TextStyle.short)
    
    def __init(self):
        super().__init__()
        self.gameID = None
        self.on_submit_interaction = None
    
    async def on_submit(self, interaction):
        self.gameID = self.game_id.value
        self.on_submit_interaction = interaction
        self.stop()