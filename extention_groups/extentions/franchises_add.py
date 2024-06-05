from models.Franchise import Franchise
from models.Channel import Channel
import discord, config, json
from database import db
from discord.ext import commands
from assets import get_free_categories
from bot import bot


with open('accepted_roles.json', 'r', encoding='utf-8') as f:
    accepted_roles = json.load(f)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='добавить', description='Добавить новую франшизу')
@discord.commands.option('город', str, required=True, parameter_name='city_name',
        description='Напишите название города франшизы',)
@discord.commands.option('регион-снг', bool, required=True,
        parameter_name='is_cis', choices=['True', 'False'],
        description='Установите значение True для региона СНГ или False для остального мира')
@discord.commands.option('каналы', str, required=True,
        parameter_name='create_channels', choices=['True', 'False'],
        description='Установите значение True, если необходимо создать стандартные каналы (менеджемент и технический)')
async def add_franchise(
        ctx: discord.ApplicationContext,
        city_name: str,
        is_cis,
        create_channels):
        
    city_name = city_name.capitalize()
    if db.query(Franchise).filter(Franchise.name == city_name).all():
        await ctx.respond('❌ Франшиза с таким именем уже существует', ephemeral=True)
        return

    if create_channels:
        channels = []
        guild: discord.Guild = bot.get_guild(config.SERVER_ID)

        if len(guild.channels) > 500 - 2:
            await ctx.respond('❌ Достикнуто максимальное количество каналов на сервере', ephemeral=True)
            return

        region = ['EN', 'RU'][is_cis]
        names = [f'TECHNICAL {region}', f'MANAGEMENT {region}']
        categories = await get_free_categories(names)

        for category, type in zip(categories, ['TECHNICAL', 'MANAGEMENT']):
            overwrites = {
                guild.get_role(i): discord.PermissionOverwrite(
                        view_channel=True, send_messages=True
                ) for i in accepted_roles[region][type]
            }
            overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=False)
            
            channel = await guild.create_text_channel(
                name=city_name,
                overwrites=overwrites,
                category=category
            )

            channels.append(Channel(id=channel.id, type=type))
    
    franchise = Franchise(name=city_name, channels=channels)
    db.add(franchise)
    db.commit()
    await ctx.respond('✅ Франшиза создана', ephemeral=True)


def setup(group: discord.SlashCommandGroup):
    add_franchise.parent = group
    group.add_command(add_franchise)