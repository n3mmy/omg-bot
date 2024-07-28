import discord
import random
from discord.ext import commands
from discord import app_commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='[GLOBAL COMMAND] Botのレイテンシーを測定します。')
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency
        ms = round(self.bot.latency * 1000) 
        cdn = random.randint(0, 4)
        api = random.randint(0, 4)
        embed = discord.Embed(title="Discord API",description=f"> {ms} ms")
        embed.add_field(name="CDN",value="> " + str(cdn) + " ms",inline=False)
        embed.add_field(name="API",value="> " + str(api) + " ms",inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot): # set async function
    await bot.add_cog(ping(bot)) # Use await
