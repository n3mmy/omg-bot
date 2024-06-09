import discord
from discord.ext import commands
from discord import app_commands

class ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='[GLOBAL COMMAND] Botのレイテンシーを測定します。')
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000) 
        await interaction.response.send_message(f'```bash\nDiscord API\n    > {latency}ms```')


async def setup(bot): # set async function
    await bot.add_cog(ping(bot)) # Use await
