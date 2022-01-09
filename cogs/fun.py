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

        if re.search(r"\bpog\b", lowered_message) and message.guild.id in self.pog_servers:
            await channel.send(file=discord.File(f"{self.bot.BASE_DIR}/resources/someone_said_pog.jpg"))

        elif "what" in lowered_message and "your favorite food" in lowered_message:
            await channel.send("Chicken nuggets, yum!")

        elif "how do i look" in lowered_message:
            await channel.send(f"If being sexy was a crime, {message.author.mention} would be a wanted criminal!")

        elif match := re.search(r"\bree+\b", lowered_message):
            match = match.string[match.start():match.end()]

            if match.count("E") >= 3:
                match = match.upper() + "E"
            else:
                match = match.lower() + "e"
            await channel.send(match)

        elif "bruh" in lowered_message:
            await channel.send("bruh")

        elif "hurb" in lowered_message:
            await channel.send("hurb")

        else:
            for word in self.TRIGGER_WORDS["bark"]["words"]:
                if re.search(rf"\b{word}\b", lowered_message):
                    await channel.send("BARK BARK BARK BARK")
                    break

    @commands.command(
        aliases=["no"]
    )
    async def stop(self, ctx, action):
        is_reply = ctx.message.reference
        image_to_load = None
        non_bark_trigger_words = {key: value for key, value in self.TRIGGER_WORDS.items() if key != "bark"}

        async with ctx.channel.typing():
            for category in non_bark_trigger_words.values():
                if action.lower() in category["words"]:
                    image_to_load = discord.File(f"{self.bot.BASE_DIR}/resources/{category['image']}")
                    break

            if image_to_load is None:
                await ctx.send(
                    f"Action: `{action}` was not recognized. Here's a list of all acceptable values:\n" +
                    "\n".join(', '.join(category["words"]) for category in non_bark_trigger_words.values())
                )
                return

            if is_reply:
                await ctx.message.delete()
                message = await ctx.channel.fetch_message(id=is_reply.message_id)
                await message.reply(file=image_to_load)
            else:
                await ctx.send(file=image_to_load)


def setup(bot):
    bot.add_cog(Fun(bot))
