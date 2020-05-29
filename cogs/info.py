import discord
import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Info(bot))
