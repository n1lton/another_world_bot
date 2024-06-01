import discord
from discord.ext import commands


@commands.slash_command(name='добавить', description='Добавить новую франшизу')
@discord.commands.option('город', str, description='Напишите название города франшизы',
        required=True, parameter_name='city_name')
@discord.commands.option('регион-снг', bool,
        description='Установите значение True для региона СНГ или False для остального мира',
        required=True, parameter_name='is_cis', choices=['True', 'False'])
@discord.commands.option('каналы', str,
        description='Установите значение True, если необходимо создать стандартные каналы (менеджемент и технический)',
        required=True, parameter_name='create_channels', choices=['True', 'False'])
async def add_franchise(
        ctx: discord.ApplicationContext,
        city_name,
        is_cis,
        create_channels):
    pass


def setup(group):
      add_franchise.parent = group
      group.add_command(add_franchise)