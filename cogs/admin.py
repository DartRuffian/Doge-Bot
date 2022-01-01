# Discord Imports
import discord
from discord.ext import commands
from discord.ext.commands import Greedy

# Eval Imports
from contextlib import redirect_stdout
import traceback
import textwrap
import io

# Other Imports
from utils import StatusType


def cleanup_code(content) -> str:
    """Removes code blocks from a given input"""
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])


class AdminOnly(commands.Cog):
    """Admin Only commands, only meant to be used by the bot author"""
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command(hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):
        """Runs code from a given code block"""
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result
        }

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except Exception:
                pass

            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                self._last_result = ret
                await ctx.send(f"```py\n{value}{ret}\n```")

    @commands.command(
        aliases=["s"],
        hidden=True
    )
    @commands.is_owner()
    async def say(self, ctx, channels: Greedy[discord.TextChannel] = None, *, message: str):
        """Basic say command, sends the message as a regular message"""
        await ctx.message.delete()
        [await channel.send(message) for channel in channels or [ctx.channel]]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        owner = self.bot.get_user(self.bot.owner_id)
        message = f"{self.bot.user.name} was just added to {guild.name!r}! Guild ID: `{guild.id}`"
        await owner.send(message)
        self.bot.logger.write(status=StatusType.OK, message=message)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        owner = self.bot.get_user(self.bot.owner_id)
        message = f"{self.bot.user.name} was just removed from {guild.name!r}! Guild ID: `{guild.id}`"
        await owner.send(message)
        self.bot.logger.write(status=StatusType.OK, message=message)


def setup(bot):
    bot.add_cog(AdminOnly(bot))
