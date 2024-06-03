import discord, config
from discord.ext import commands
from database import db, Franchise, User, Channel
from bot import bot
from assets import get_franchises


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='удалить', description='Удалить существующую франшизу')
@discord.commands.option('франшиза', str, required=True,
        parameter_name='franchise_name', autocomplete=get_franchises,
        description='Напишите название города франшизы для поиска')
@discord.commands.option('удалить-с-сервера', str, required=True,
        parameter_name='delete_partner', choices=['True', 'False'],
        description='Установите значение True, если необходимо удалить партнёра с сервера',)
async def delete_franchise(ctx: discord.ApplicationContext, franchise_name, delete_partner):
    guild = bot.get_guild(config.SERVER_ID)

    if delete_partner:
        data = db.query(User).filter(User.franchise_name == franchise_name).all()
        for partner in data:
            member = guild.get_member(partner.id)
            await member.ban(reason=f'Удаление франшизы {franchise_name}')

    franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()
    for channel in franchise.channels:
        if channel == -1:
            continue

        discord_channel = guild.get_channel(channel.id)

        if discord_channel.category and len(discord_channel.category.channels) == 1:
            await discord_channel.category.delete(reason=f'Удаление франшизы {franchise_name}')

        await discord_channel.delete(reason=f'Удаление франшизы {franchise_name}')

    db.delete(franchise)
    db.commit()

    await ctx.respond('✅ Франшиза удалена', ephemeral=True)


def setup(group: discord.SlashCommandGroup):
      delete_franchise.parent = group
      group.add_command(delete_franchise)