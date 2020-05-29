import discord
from discord.ext import commands


class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return
        ignored = (commands.CommandNotFound, commands.NotOwner)
        if isinstance(error, ignored):
            return
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'🚫 | {ctx.command} can not be used in Private Messages. (DM)')
            except:
                pass

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("⛔ | I don\'t have permission!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send('🚫 | Bad Argument. Try Again.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('🙄 | You don\'t have permission to do this.')
        elif isinstance(error, commands.CommandOnCooldown):
            tt = ""
            if error.retry_after < 60:
                tt = str(round(error.retry_after, 2)) + " Seconds"
            if error.retry_after > 60 and error.retry_after < 3600:
                min = int(error.retry_after) // 60
                sec = int(error.retry_after) % 60
                tt = str(min) + " Minute(s) and " + str(sec) + " Seconds"

            embed = discord.Embed(title='🕝 | Slow down!', description=f"This command can be used again in **{tt}**")
            embed.set_footer(text=f"ctx.author.name")

            msg = await ctx.send(embed=embed)
            await asyncio.sleep(error.retry_after)
            await msg.delete(delay=3)
        else:
            #un handled
            await ctx.send(f"Playing with errors: \n \n ```\n{error}``` \n \n Type: {type(error)}")
            
def setup(bot):
    bot.add_cog(error_handler(bot))
