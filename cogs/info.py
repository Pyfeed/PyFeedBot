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


def setup(bot):
    bot.add_cog(Info(bot))
