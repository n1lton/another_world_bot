import config, discord
from discord.ext import commands


bot = commands.Bot(
    command_prefix=config.PREFIX,
    intents=discord.Intents.all(),
    debug_guilds=[config.SERVER_ID]
)


@bot.event
async def on_ready():
    print('Bot is running.')
