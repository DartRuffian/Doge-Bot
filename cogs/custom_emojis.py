# Discord Imports
import discord
from discord.ext import commands


class CustomEmojis(commands.Cog, name="Custom Emojis"):
    """Simple Container for the Bot's custom emojis"""
    def __init__(self, bot):
        self.bot = bot
        self.reload_emojis()

    def reload_emojis(self):
        """Load all custom emojis from the Emoji Hub server to a dictionary"""
        self.bot.custom_emojis = {emoji.name: emoji for emoji in self.bot.get_guild(903452394204065833).emojis}

    @commands.command(hidden=True)
    @commands.is_owner()
    async def admin_clone(self, emoji: discord.Emoji):
        emoji_hub = self.bot.get_guild(903452394204065833)
        await emoji_hub.create_custom_emoji(name=emoji.name, image=await emoji.url.read())


def setup(bot):
    bot.add_cog(ClassName(bot))
