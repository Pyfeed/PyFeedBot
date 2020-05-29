import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import random
from utils.game_classes import Connect4
from utils.game_classes import HangmanGameClass as HMGame


colour = 0xfffca6

class Games(commands.Cog, name='Games'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["c4"])
    @commands.bot_has_permissions(add_reactions=True)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def connect4(self, ctx, member: discord.Member):
        if member == ctx.author or member.bot:
            return await ctx.send("You cannot play against yourself or a bot.")

        c = await ctx.send(f"{member.mention} agree to play?")
        await c.add_reaction("✅")
        await c.add_reaction("❌")
        await asyncio.sleep(1)

        def check(reaction, user):
            return user == member and str(reaction.emoji) in ['✅', '❌']
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("Game canceled.")
        else:
            if str(reaction.emoji) == '✅':
                pass
            elif str(reaction.emoji) == '❌':
                return await ctx.send("Game denied.")

        player1 = random.choice([ctx.author, member])
        player2 = member if player1 == ctx.author else ctx.author

        game = Connect4(player1, player2)
        winner = await game.run(ctx)
        if winner:
            if isinstance(winner, tuple):
                await ctx.send(f"{player1.mention} and {player2.mention} tied")
            else:
                await ctx.send(f"{winner.mention} has won.")
        else:
            await ctx.send("No one made a move.")



    games = {}
    pending_games = []

    def create_hangman_game(self, word, ctx):
        # Create a new game, then save it as the server's game
        game = HMGame(word)
        self.games[ctx.message.guild.id] = game
        game.author = ctx.message.author.id
        return game

    @commands.group(aliases=['hm'], invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, BucketType.user)
    async def hangman(self, ctx, *, guess):
        """Makes a guess towards the server's currently running hangman game
        EXAMPLE: !hangman e (or) !hangman The Phrase!"""
        game = self.games.get(ctx.message.guild.id)
        if not game:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("There are currently no hangman games running!")
            return
        if game.author == ctx.message.author.id:
            await ctx.send("You cannot guess on your own hangman game!")
            return

        # Check if we are guessing a letter or a phrase. Only one letter can be guessed at a time
        # So if anything more than one was provided, we're guessing at the phrase
        # We're creating a fmt variable, so that we can  add a message for if a guess was correct or not
        # And also add a message for a loss/win
        if len(guess) == 1:
            if guess.lower() in game.guessed_letters:
                ctx.command.reset_cooldown(ctx)
                await ctx.send("That letter has already been guessed!")
                # Return here as we don't want to count this as a failure
                return
            if game.guess_letter(guess):
                fmt = "That's correct!"
            else:
                fmt = "Sorry, that letter is not in the phrase..."
        else:
            if game.guess_word(guess):
                fmt = "That's correct!"
            else:
                fmt = "Sorry that's not the correct phrase..."

        if game.win():
            fmt += " You guys got it! The phrase was `{}`".format(game.word)
            del self.games[ctx.message.guild.id]
        elif game.failed():
            fmt += " Sorry, you guys failed...the phrase was `{}`".format(game.word)
            del self.games[ctx.message.guild.id]
        else:
            fmt += str(game)

        await ctx.send(fmt)

    @hangman.command(name='create', aliases=['start'])
    @commands.guild_only()
    @commands.cooldown(1, 30, BucketType.guild)
    async def create_hangman(self, ctx):
        """This is used to create a new hangman game"""

        # Only have one hangman game per server, since anyone
        # In a server (except the creator) can guess towards the current game
        if self.games.get(ctx.message.guild.id) is not None:
            await ctx.send("Sorry but only one Hangman game can be running per server!")
            return
        if ctx.guild.id in self.pending_games:
            await ctx.send("Someone has already started one, and I'm now waiting for them...")
            return

        try:
            msg = await ctx.message.author.send(
                "Please respond with a phrase you would like to use for your hangman game in **{}**\n\nPlease keep "
                "phrases less than 31 characters".format(
                    ctx.message.guild.name))
        except discord.Forbidden:
            await ctx.send(
                "I can't message you {}! Please allow DM's so I can message you and ask for the hangman phrase you "
                "want to use!".format(ctx.message.author.display_name))
            return

        await ctx.send("I have DM'd you {}, please respond there with the phrase you would like to setup".format(
            ctx.message.author.display_name))

        def check(m):
            return m.channel == msg.channel and len(m.content) <= 30

        self.pending_games.append(ctx.guild.id)
        try:
            msg = await ctx.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            self.pending_games.remove(ctx.guild.id)
            await ctx.send(
                "You took too long! Please look at your DM's as that's where I'm asking for the phrase you want to use")
            return
        else:
            self.pending_games.remove(ctx.guild.id)

        forbidden_phrases = ['stop', 'delete', 'remove', 'end', 'create', 'start']
        if msg.content in forbidden_phrases:
            await ctx.send("Detected forbidden hangman phrase; current forbidden phrases are: \n{}".format(
                "\n".join(forbidden_phrases)))
            return

        game = self.create_hangman_game(msg.content, ctx)
        # Let them know the game has started, then print the current game so that the blanks are shown
        await ctx.send(
            "Alright, a hangman game has just started, you can start guessing now!\n{}".format(str(game)))

    @hangman.command(name='delete', aliases=['stop', 'remove', 'end'])
    @commands.guild_only()
    @commands.cooldown(1, 30, BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def stop_hangman(self, ctx):
        """Force stops a game of hangman"""
        if self.games.get(ctx.message.guild.id) is None:
            await ctx.send("There are no Hangman games running on this server!")
            return

        del self.games[ctx.message.guild.id]
        await ctx.send("I have just stopped the game of Hangman, a new should be able to be started now!")


def setup(bot):
    bot.add_cog(Games(bot))
