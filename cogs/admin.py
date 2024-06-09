import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import json

class admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    class MyView(View):
        @discord.ui.button(label="❌ Close", style=discord.ButtonStyle.danger, custom_id="danger_button")
        async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
            if self.user_id == interaction.user.id:
                await interaction.message.delete()

    def remove_key_from_json(json_data, key):
        if isinstance(json_data, dict):
            if key in json_data:
                del json_data[key]
            for k, v in list(json_data.items()):
                remove_key_from_json(v, key)
        elif isinstance(json_data, list):
            for item in json_data:
                remove_key_from_json(item, key)

    @app_commands.command(name='admin', description='[ADMIN COMMAND] パネルを表示します。')
    async def perm(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Admin Panel", description="管理用パネルです。", color=discord.Color.blurple())
        view = self.MyView()
        await interaction.response.send_message(embed=embed, view=view)
        

async def setup(bot):
    await bot.add_cog(admin(bot))