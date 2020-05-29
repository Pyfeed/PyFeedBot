from itertools import cycle
from typing import Optional, Tuple, Union

import discord
import numpy
from discord.ext import menus

# Connect 4
class Connect4(menus.Menu):
    filler = "\N{BLACK LARGE SQUARE}"
    red = "\N{LARGE RED CIRCLE}"
    blue = "\N{LARGE BLUE CIRCLE}"
    numbers = [str(i) + "\N{VARIATION SELECTOR-16}\u20e3" for i in range(1, 8)]

    def __init__(self, player1: discord.Member, player2: discord.Member, **kwargs):
        super().__init__(**kwargs)
        self.players = (player1, player2)
        self._player_ids = {p.id for p in self.players}
        self.player_cycle = cycle(self.players)
        self.current_player = next(self.player_cycle)
        self.last_move = None
        self.winner = None
        # noinspection PyTypeChecker
        self.board = numpy.full((6, 7), self.filler)
        # This is kinda hacky but /shrug
        for button in [
            menus.Button(num, self.do_number_button) for num in self.numbers
        ]:
            self.add_button(button)

    def reaction_check(self, payload):
        if payload.message_id != self.message.id:
            return False

        if payload.user_id != self.current_player.id:
            return False

        return payload.emoji in self.buttons

    async def send_initial_message(self, ctx, channel):
        return await channel.send(self.discord_message)

    async def do_number_button(self, payload):
        move_column = self.numbers.index(payload.emoji.name)
        move_row = self.free(move_column)

        # self.free returns None if the column was full
        if move_row is not None:
            self.make_move(move_row, move_column)

            # timeouts count as wins
            self.winner = self.current_player

            if self.check_wins():
                self.winner = self.current_player
                self.stop()

            # Tie
            if self.filler not in self.board:
                self.winner = self.players
                self.stop()

            self.current_player = next(self.player_cycle)
            await self.message.edit(content=self.discord_message)

    @menus.button("\N{BLACK DOWN-POINTING DOUBLE TRIANGLE}", position=menus.Last())
    async def do_resend(self, _):
        await self.message.delete()
        self.message = msg = await self.send_initial_message(self.ctx, self.ctx.channel)
        for emoji in self.buttons:
            await msg.add_reaction(emoji)

    @menus.button("\N{CROSS MARK}", position=menus.Last(1))
    async def do_cancel(self, _):
        self.stop()

    @property
    def current_piece(self):
        if self.current_player == self.players[0]:
            return self.red
        else:
            return self.blue

    @property
    def board_message(self):
        """
        The string representing the board for discord
        """
        msg = "\n".join(["".join(i) for i in self.board])
        msg += "\n"
        msg += "".join(self.numbers)
        return msg

    # @property
    # def embed(self):
    #     """
    #     The embed to send to discord
    #     """
    #     board_embed = discord.Embed(description=self.board_message)
    #
    #     if self.last_move is not None:
    #         board_embed.add_field(name="Last move", value=self.last_move, inline=False)
    #
    #     if self._running:
    #         board_embed.add_field(
    #             name="Current turn", value=self.current_player.mention
    #         )
    #
    #     return board_embed

    @property
    def discord_message(self):
        final = ""

        if self.last_move is not None:
            final += "Last move:\n"
            final += self.last_move
            final += "\n"

        if self._running:
            final += "Current turn:\n"
            final += self.current_piece + self.current_player.mention
            final += "\n"

        final += self.board_message

        return final

    def free(self, num: int):
        for i in range(5, -1, -1):
            if self.board[i][num] == self.filler:
                return i

    def make_move(self, row: int, column: int):
        self.board[row][column] = self.current_piece
        self.last_move = (
            f"{self.current_piece}{self.current_player.mention} ({column + 1})"
        )

    def check_wins(self):
        def check(array: list):
            array = list(array)
            for i in range(len(array) - 3):
                if array[i: i + 4].count(self.current_piece) == 4:
                    return True

        for row in self.board:
            if check(row):
                return True

        for column in self.board.T:
            if check(column):
                return True

        def get_diagonals(matrix: numpy.ndarray):
            dias = []
            for offset in range(-2, 4):
                dias.append(list(matrix.diagonal(offset)))
            return dias

        for diagonal in [
            *get_diagonals(self.board),
            *get_diagonals(numpy.fliplr(self.board)),
        ]:
            if check(diagonal):
                return True

    async def run(self, ctx) -> Optional[Union[discord.Member, Tuple[discord.Member]]]:
        """
        Run the game and return the winner(s)
        returns None if the first player never made a move
        """
        await self.start(ctx, wait=True)
        return self.winner

import re
# Hangman
# For some reason it only works when in a separate file only for hangman (at lest for AliBot)
class HangmanGameClass():
    def __init__(self, word):
        self.word = word
        # This converts everything but spaces to a blank
        self.blanks = "".join(letter if not re.search("[a-zA-Z0-9]", letter) else "_" for letter in word)
        self.failed_letters = []
        self.guessed_letters = []
        self.fails = 0

    def guess_letter(self, letter):
        # No matter what, add this to guessed letters so we only have to do one check if a letter was already guessed
        self.guessed_letters.append(letter)
        if letter.lower() in self.word.lower():
            # Replace every occurence of the guessed letter, with the correct letter
            # Use the one in the word instead of letter, due to capitalization
            self.blanks = "".join(
                word_letter if letter.lower() == word_letter.lower() else self.blanks[i] for i, word_letter in
                enumerate(self.word))
            return True
        else:
            self.fails += 1
            self.failed_letters.append(letter)
            return False

    def guess_word(self, word):
        if word.lower() == self.word.lower():
            self.blanks = self.word
            return True
        else:
            self.fails += 1
            return False

    def win(self):
        return self.word == self.blanks

    def failed(self):
        return self.fails == 7

    def __str__(self):
        # Here's our fancy formatting for the hangman picture
        # Each position in the hangman picture is either a space, or part of the man, based on how many fails there are
        man = "     ——\n"
        man += "    |  |\n"
        man += "    {}  |\n".format("o" if self.fails > 0 else " ")
        man += "   {}{}{} |\n".format("/" if self.fails > 1 else " ", "|" if self.fails > 2 else " ",
                                      "\\" if self.fails > 3 else " ")
        man += "    {}  |\n".format("|" if self.fails > 4 else " ")
        man += "   {} {} |\n".format("/" if self.fails > 5 else " ", "\\" if self.fails > 6 else " ")
        man += "       |\n"
        man += "    ———————\n"
        fmt = "```\n{}```".format(man)
        # Then just add the guesses and the blanks to the string
        fmt += "```\nGuesses: {}\nWord: {}```".format(", ".join(self.failed_letters), " ".join(self.blanks))
        return fmt

