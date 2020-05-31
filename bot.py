import os
import json
import logging
logging.basicConfig(format="[%(levelname)s] [%(asctime)s] %(message)s")
import discord
from discord.ext import commands

with open("config.json", "r") as fh:
    data = json.load(fh)

class PyFeed(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=data["prefix"])
        self.logger = logging.getLogger(__name__)

        for ext in os.listdir('./cogs'):
            if ext.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{ext[:-3]}")
                    self.logger.info(f"Extension {ext[:-3]} loaded!")
                except Exception as e:
                    self.logger.critical(f"Extension {ext[:-3]} could not be loaded because:\n{e}")

    async def on_ready(self):
        self.logger.info("Bot is Started!")

bot = PyFeed()
bot.run(data["token"])