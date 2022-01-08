# Discord Imports
import discord
from discord.ext import commands

# Other Imports
from datetime import datetime


def create_embed(*, color: str, message: str, footer: str = None, author_info: dict = None, fields: dict = None) -> discord.Embed:
    color_list = {
        "red": 0xf84b51,
        "orange": 0xe6852b,
        "green": 0x5fe468
    }
    embed = discord.Embed(
        description=message,
        color=color_list.get(color),
        timestamp=datetime.now()
    )
    if fields is not None:
        for key, value in fields.items():
            embed.add_field(name=key, value=value, inline=False)
    if author_info is not None:
        embed.set_author(
            name=author_info["name"],
            icon_url=author_info["icon_url"]
        )
    embed.set_footer(text=footer or "")
    return embed


def check_guild(guild_id: int) -> bool:
    return guild_id in [905278647596879913, 929030336585814106]


class JesterLogging(commands.Cog, name="Jester Logging"):
    """Sends a message to another server to log message deletion and message editing"""
    def __init__(self, bot):
        self.bot = bot
        self.guild = 929030336585814106
        self.log_channel = 929031095012458527

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(self.guild)
        self.log_channel = self.guild.get_channel(self.log_channel)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not check_guild(message.guild.id):
            return

        await self.log_channel.send(
            embed=create_embed(
                color="red",
                message=f"The message sent by `{message.author}` in {message.channel.mention} was deleted.",
                footer=f"Server: {message.guild.name}\nMessage ID: {message.id}",
                author_info={"name": message.author, "icon_url": message.author.avatar_url},
                fields={"Message": message.content or '`None`'}
            )
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not check_guild(before.guild.id):
            return

        if not (before.content and after.content):
            return

        await self.log_channel.send(
            embed=create_embed(
                color="orange",
                message=f"`{before.author}` edited their [message]({before.jump_url}) in {before.channel.mention}",
                footer=f"Server: {before.guild.name}\nMessage ID: {before.id}",
                author_info={"name": before.author, "icon_url": before.author.avatar_url},
                fields={"Before": before.content, "After": after.content}
            )
        )


def setup(bot):
    bot.add_cog(JesterLogging(bot))
