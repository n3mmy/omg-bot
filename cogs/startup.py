import discord
from discord import app_commands
from discord.ext import commands
import time

class startup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.owner_ids = [1178498830505885787]
        await self.bot.tree.sync()
        await self.bot.load_extension("jishaku")
        await self.bot.change_presence(activity=discord.Streaming(name=f"nemcloud.net | {len(self.bot.guilds)} guilds", url="https://x.com/nemmy2_"), status=discord.Status.idle)
        print("[INFO] Ready!")

async def setup(bot: commands.Bot):
    await bot.add_cog(startup(bot))
