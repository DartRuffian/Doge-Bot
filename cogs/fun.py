# Discord Imports
import discord
from discord.ext import commands

# Other Imports
import json
import re


class Fun(commands.Cog, name="Jokes and Fun!"):
    """Commands and message events meant to spark joy"""
    def __init__(self, bot):
        self.bot = bot
        self.pog_servers = self.load_pog_servers()
        self.TRIGGER_WORDS = self.load_trigger_words()

    def load_pog_servers(self):
        with open(f"{self.bot.BASE_DIR}/resources/pog_servers.json", "r") as f:
            servers = json.load(f)
        return servers

    def load_trigger_words(self):
        with open(f"{self.bot.BASE_DIR}/resources/trigger_words.json", "r") as f:
            words = json.load(f)
        return words

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        lowered_message = message.content.lower()
        channel = message.channel

        if "pog" in lowered_message and message.guild.id in self.pog_servers:
            await channel.send(file=discord.File(f"{self.bot.BASE_DIR}/resources/someone_said_pog.jpg"))

        elif "what" in lowered_message and "your favorite food" in lowered_message:
            await channel.send("Chicken nuggets, yum!")

        elif "how do i look" in lowered_message:
            await channel.send(f"If being sexy was a crime, {message.author.mention} would be a law abiding citizen")

        elif re.search(r"\bree+\b", lowered_message):
            match = re.search(r"\bree+\b", lowered_message).string
            await channel.send(match + "E" if match.count("E") >= 3 else "e")

        elif "bruh" in lowered_message:
            await channel.send("bruh")

        elif "hurb" in lowered_message:
            await channel.send("hurb")

        else:
            for word in self.TRIGGER_WORDS["bark"]:
                if re.search(rf"\b{word}\b", lowered_message):
                    await channel.send("BARK BARK BARK BARK")
                    break

    @commands.command(
        aliases=["no"]
    )
    async def stop(self, ctx, action):
        is_reply = ctx.message.reference

        if action.lower() in self.TRIGGER_WORDS["horny"]:
            image = discord.File(f"{self.bot.BASE_DIR}/resources/no_horny.jpg")
        elif action.lower() in self.TRIGGER_WORDS["drinking"]:
            image = discord.File(f"{self.bot.BASE_DIR}/resources/no_drinking.jpg")
        else:
            await ctx.send(
                f"Action: `{action}` was not recognized. Here's a list of all acceptable values:\n" +
                "\n".join(horny_terms + drinking_terms)
            )
            return

        if is_reply:
            await ctx.message.delete()
            message = await ctx.channel.fetch_message(id=is_reply.message_id)
            await message.reply(file=image)
        else:
            await ctx.send(file=image)

    @commands.command()
    async def pet(self, ctx):
        await ctx.send(":D\n*tail wagging sounds*")


def setup(bot):
    bot.add_cog(Fun(bot))
