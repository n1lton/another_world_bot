import discord, os
from discord.ext import commands
from bot import bot

franchises = discord.SlashCommandGroup(
    name='франшизы'
)

for filename in os.listdir('extentions_groups/extentions'):
    if filename.endswith('.py') and filename.startswith('franchises_'):
        module = __import__(f'extentions_groups.extentions.{filename.removesuffix(".py")}', fromlist=['setup'])
        module.setup(franchises)

def setup(bot: commands.Bot):
    bot.add_application_command(franchises)