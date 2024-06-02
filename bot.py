import config, discord
from discord.ext import commands


bot = commands.Bot(
    command_prefix=config.PREFIX,
    intents=discord.Intents.all(),
    debug_guilds=[1246394608972206143]
)


@bot.event
async def on_ready():
    print('Bot is running.')
