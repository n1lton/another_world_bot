from models.User import User
from models.Franchise import Franchise
from models.Channel import Channel
import discord, config
from discord.ext import commands
from database import db
from bot import bot
from autocomplete import get_franchises


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='удалить', description='Удалить существующую франшизу')
@discord.commands.option('франшиза', str, required=True,
        parameter_name='franchise_name', autocomplete=get_franchises,
        description='Напишите название города франшизы для поиска')
@discord.commands.option('удалить-с-сервера', bool, required=True,
        parameter_name='delete_users', choices=['True', 'False'],
        description='Установите значение True, если необходимо удалить партнёров с сервера',)
async def delete_franchise(ctx: discord.ApplicationContext, franchise_name, delete_users):
    franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()

    if not franchise:
        await ctx.respond('❌ Франшиза не найдена', ephemeral=True)
        return

    guild = bot.get_guild(config.SERVER_ID)
    if delete_users:
        for user in franchise.users:
            member = guild.get_member(user.id)
            await member.kick(reason=f'Удаление франшизы {franchise_name}')

    for channel in franchise.channels:
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