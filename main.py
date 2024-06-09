import os
import discord
from discord import app_commands
from discord.ext import commands
from env.config import Config

config = Config()

TOKEN = config.token

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="o!", intents=discord.Intents.all())

    async def startup(self):
        bot.owner_ids = [1178498830505885787]
        await bot.wait_until_ready()
        await bot.tree.sync()
        await bot.change_presence(activity=discord.Game("Booting..."), status=discord.Status.dnd)
        print('[INFO] Sucessfully synced applications commands')
        print(f'[INFO] Connected as {bot.user}')

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"[INFO] Loaded {filename}")
                except Exception as e:
                    print(f"[WARNING] Failed to load {filename}")
                    print(f"[ERROR] {e}")
        self.loop.create_task(self.startup())


bot = Bot()


bot.run(TOKEN)
