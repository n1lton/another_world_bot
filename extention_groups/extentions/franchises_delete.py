import discord, config
from discord.ext import commands
from database import db, Franchise, Partner, Channel
from bot import bot


def get_cities(ctx: discord.AutocompleteContext):
    data = db.query(Franchise).all()
    return [i.name for i in data if i.name.startswith(ctx.value.lower())]


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='удалить', description='Удалить существующую франшизу')
@discord.commands.option('найти-город', str,
        description='Напишите название города франшизы для поиска',
        required=True, parameter_name='city_name', autocomplete=get_cities)
@discord.commands.option('удалить-с-сервера', str,
        description='Установите значение True, если необходимо удалить партнёра с сервера',
        required=True, parameter_name='delete_partner', choices=['True', 'False'])
async def delete_franchise(ctx: discord.ApplicationContext, city_name, delete_partner):
    guild = bot.get_guild(config.SERVER_ID)

    if delete_partner:
        data = db.query(Partner).filter(Partner.franchise_name == city_name).all()
        for partner in data:
            member = guild.get_member(partner.id)
            await member.ban(reason=f'Удаление франшизы {city_name}')

    franchise = db.query(Franchise).filter(Franchise.name == city_name).first()
    for channel in franchise.channels:
        if channel == -1:
            continue

        discord_channel = guild.get_channel(channel.id)

        if discord_channel.category and len(discord_channel.category.channels) == 1:
            await discord_channel.category.delete(reason=f'Удаление франшизы {city_name}')

        await discord_channel.delete(reason=f'Удаление франшизы {city_name}')

    db.delete(franchise)
    db.commit()

    await ctx.respond('✅ Франшиза удалена', ephemeral=True)


def setup(group: discord.SlashCommandGroup):
      delete_franchise.parent = group
      group.add_command(delete_franchise)