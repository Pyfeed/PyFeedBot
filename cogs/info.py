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
            
         @commands.command()
        async def Uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

        @commands.group(invoke_without_command=True, name='About', description='About PyFeed Bot', case_insensitive=True)
        async def about_command(self, ctx):
            embed = discord.Embed(title='PyFeed Bot', description=f'{self.bot.user.mention}')
            embed.add_field(name='**About**',
                            value=f'To be added to')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
