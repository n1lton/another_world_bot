import discord
from discord.ext import commands


franchises = discord.SlashCommandGroup(
    name='франшизы'
)

@franchises.command(name='добавить', description='Добавить новую франшизу')
@discord.commands.option('город', str, description='Напишите название города франшизы',
        required=True, parameter_name='city_name')
@discord.commands.option('регион-снг', bool,
        description='Установите значение True для региона СНГ или False для остального мира',
        required=True, parameter_name='is_cis', choices=[True, False])
@discord.commands.option('каналы', str,
        description='Установите значение True, если необходимо создать стандартные каналы (менеджемент и технический)',
        required=True, parameter_name='create_channels', choices=[True, False])
async def add_franchise(
        ctx: discord.ApplicationContext,
        city_name,
        is_cis,
        create_channels):
    pass

def setup(bot: commands.Bot):
    bot.add_application_command(franchises)