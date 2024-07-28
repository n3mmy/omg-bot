import discord
import os
import re
import json
import time
from discord.ext import commands
from discord import app_commands
from env.config import Config

config = Config()

OWNER = config.owner

def perm_list():
    data = {}
    if os.path.exists("./env/admin.json"):
        with open("./env/admin.json", 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass
    return data

def perm_level(level):
    result = []
    for key, value in perm_list().items():
        if value == str(level):
            result.append(int(key))
    return result

def perm_add(userid, level):
    data = {}
    if os.path.exists("./env/admin.json"):
        with open("./env/admin.json", 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass
    data[userid] = level
    with open("./env/admin.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def perm_del(userid):
    data = {}
    if os.path.exists("./env/admin.json"):
        with open("./env/admin.json", 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                pass
    if userid in data:
        del data[userid]
    with open("./env/admin.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx):
        if ctx.message.author.id in perm_level(3) or ctx.message.author.id in perm_level(2) or ctx.message.author.id in perm_level(1):
            await ctx.message.add_reaction("🔄")
            message_content = ctx.message.content
            match = re.search(r'<@!?(\d+)> (\d+)', message_content)
            if match:
                userid = match.group(1)
                level = match.group(2)
                if level in ['1', '2', '3'] and level == "1":
                    if ctx.message.author.id in perm_level(2) or ctx.message.author.id in perm_level(3):
                        perm_add(userid, level)
                        await ctx.send(f'<@{userid}> に Level 1 権限を付与しました。')
                        await ctx.message.add_reaction("✅")
                    else:
                        await ctx.message.add_reaction("❌")
                elif level in ["1","2","3"] and level == "2":
                    if ctx.message.author.id in perm_level(3):
                        perm_add(userid, level)
                        await ctx.send(f'<@{userid}> に Level 2 権限を付与しました。')
                        await ctx.message.add_reaction("✅")
                    else:
                        await ctx.message.add_reaction("❌")
                elif level in ["1","2","3"] and level == "3":
                    if ctx.message.author.id in self.bot.owner_ids:
                        perm_add(userid, level)
                        await ctx.send(f'<@{userid}> に Level 3 権限を付与しました。')
                        await ctx.message.add_reaction("✅")
                    else:
                        await ctx.message.add_reaction("❌")
                else:
                    await ctx.message.add_reaction("❌")
            else:
                await ctx.message.add_reaction("❌")

    @commands.command()
    async def remove(self, ctx):
        if ctx.message.author.id in perm_level(3):
            await ctx.message.add_reaction("🔄")
            message_content = ctx.message.content
            match = re.search(r'<@!?(\d+)>', message_content)
            if match:
                userid = match.group(1)
                perm_del(userid)
                await ctx.send(f'<@{userid}> の Admin 権限を削除しました。')
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.add_reaction("❌")
        else:
            await ctx.message.add_reaction("❌")

    @commands.command()
    async def users(self, ctx):
        if ctx.message.author.id in perm_level(1) or ctx.message.author.id in perm_level(2) or ctx.message.author.id in perm_level(3):
            embed = discord.Embed(title="Owner",description=str(OWNER))
            embed.add_field(name="Permission Level 3",value=str(perm_level(3)),inline=False)
            embed.add_field(name="Permission Level 2",value=str(perm_level(2)),inline=False)
            embed.add_field(name="Permission Level 1",value=str(perm_level(1)),inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def shutdown(self, ctx):
        print(perm_level(2))
        if ctx.message.author.id in perm_level(3):
            await ctx.send("Bye 👋 5秒後に終了します。")
            time.sleep(5)
            exit()

    @commands.command()
    async def delete(self, ctx):
        await ctx.message.add_reaction("🔄")
        if ctx.message.reference:
            replied_message = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            if self.bot.user.id:
                await replied_message.delete()
                await ctx.message.add_reaction("✅")
            elif ctx.message.author.id in perm_level(2) or ctx.message.author.id in perm_level(3):
                await replied_message.delete()
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.add_reaction("❌")
        else:
            await ctx.message.add_reaction("❌")

async def setup(bot):
    await bot.add_cog(admin(bot))