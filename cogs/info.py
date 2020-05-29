import discord
import datetime
import time
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.command()
        async def ping(self, ctx):
            start = time.perf_counter()
            message = await ctx.send("Ping...")
            end = time.perf_counter()
            duration = (end - start) * 1000
            await message.edit(content='Pong! {:.2f}ms'.format(duration))

        @commands.group(invoke_without_command=True, name='About', description='About PyFeed Bot', case_insensitive=True)
        async def about_command(self, ctx):
        embed = discord.Embed(title='PyFeed Bot', description=f'{self.bot.user.mention}')
        embed.add_field(name='**About**',
                        value=f'To be added to')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
