# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from math import log


class Formulas(commands.Cog, name="Useful Formulas"):
    """description"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        brief="Calculates the chance for you to catch a shiny of the Pokémon you're shiny hunting.",
        aliases=["shiny%"]
    )
    async def shiny_chance(self, ctx, streak: int = None):
        if streak is None:
            await ctx.reply("""You need to include your current shiny chain for the Pokémon you're hunting.
You can view it by doing **`p!sh`**.""")
            return
        chance = 1 + log(1 + streak / 30)
        await ctx.reply(f"With a chain of {streak}, you have a {round(chance, 2)}% to encounter a shiny!")


def setup(bot):
    bot.add_cog(Formulas(bot))
