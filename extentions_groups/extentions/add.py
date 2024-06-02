import discord, config, json
from database import cur
from discord.ext import commands
from assets import get_free_categories
from bot import bot


with open('accepted_roles.json', 'r', encoding='utf-8') as f:
        accepted_roles = json.load(f)


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
    channel_ids = [-1, -1]
    if create_channels:
        region = ['EN', 'RU'][is_cis]
        names = [f'TECHNICAL {region}', f'MANAGEMENT {region}']
        categories = await get_free_categories(names)

        guild: discord.Guild = bot.get_guild(config.SERVER_ID)

        for index, (category, name) in enumerate(zip(categories, ['TECHNICAL', 'MANAGEMENT'])):
                overwrites = {
                        guild.get_role(i): discord.PermissionOverwrite(
                                view_channel=True, send_messages=True
                        ) for i in accepted_roles[region][name]
                }
                overwrites[guild.default_role] = discord.PermissionOverwrite(
                        view_channel=False
                )
                channel = await guild.create_text_channel(
                        name=city_name,
                        overwrites=overwrites,
                        category=category
                )

                channel_ids[index] = channel.id
        
        cur.execute(f'INSERT INTO franchises VALUES (?, ?, ?)', (city_name, *channel_ids))
        await ctx.respond('✅ Франшиза создана', ephemeral=True)


def setup(group: discord.SlashCommandGroup):
      add_franchise.parent = group
      group.add_command(add_franchise)