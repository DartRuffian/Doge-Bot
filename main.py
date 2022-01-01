"""Main Bot File"""
# Discord Imports
import discord
from discord.ext import commands

# Keep Bot Online
from webserver import keep_alive

# Other Imports
from datetime import datetime
from utils import Logger
from os import getcwd, listdir, environ


def get_token() -> str:
    """Loads the bot's token either from a local file or environment variable"""
    try:
        # If running locally
        with open("token.txt", "r") as f:
            token = f.read().split("\n")[0]
    except FileNotFoundError:
        # If running on server
        token = environ.get("DISCORD_BOT_SECRET")

    return token


def main() -> None:
    TOKEN = get_token()

    # Define the bot
    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True
    intents.emojis = True
    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("+"),
        owner_id=400337254989430784,
        activity=discord.Game("with my tail!"),
        case_insensitive=True,
        intents=intents,
    )

    # Custom Attributes
    bot.BASE_DIR = getcwd()
    bot.EMBED_COLOR = 0x0E151D
    bot.LAUNCH_TIME = datetime.utcnow()
    bot.logger = Logger(bot, f"{bot.BASE_DIR}/resources/bot.log")

    # Load all cogs
    for filename in listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    @bot.event
    async def on_ready():
        # Called whenever the bot connects to Discord
        print("Logged in")
        print(f"Username: {bot.user.name}")
        print(f"User Id : {bot.user.id}")

    keep_alive()
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
