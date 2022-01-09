# Discord Imports
import discord
from discord.ext import commands

# Fetch Imports
from random import choice, randint
import re


class Games(commands.Cog, name="Play Games with Doge! :D"):
    """Interact with Doge, you can pet him, feed him, and play fetch!"""
    def __init__(self, bot):
        self.bot = bot
        self.fetch_items = self.load_fetch_items()

    def load_fetch_items(self) -> list:
        with open(f"{self.bot.BASE_DIR}/resources/fetch_items.txt") as f:
            fetch_items = [line.strip("\n") for line in f.readlines() if not line.startswith("#")]
        return fetch_items

    @commands.command()
    async def pet(self, ctx):
        await ctx.send(":D\n*tail wagging sounds*")

    @commands.command()
    async def treat(self, ctx, *, food: str = ""):
        if "chicken nugget" in food.lower():
            await ctx.send("My favorite snack!\n*nom nom nom*")
        else:
            await ctx.send("Thank you for the treat! :D\nBut do you know my favorite treat?")

    @commands.command()
    async def fetch(self, ctx):
        item = choice(self.fetch_items)
        item = item.replace(
            "<member>",
            choice(ctx.guild.members).mention
        )
        if match := re.search(r"<number:\d+:\d+>", item):
            match = match.string[match.start():match.end()]
            min_val, max_val = match.strip("<number:>").split(":")
            random_number = str(randint(int(min_val), int(max_val)))
            item = item.replace(match, random_number)

        await ctx.send(f"You throw a stick to Doge, and Doge brings back {item}!")


def setup(bot):
    bot.add_cog(Games(bot))