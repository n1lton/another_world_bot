from models.Franchise import Franchise
from models.Channel import Channel
import discord, config
from discord.ext import commands
from database import db
from assets import get_free_categories, get_franchises
from bot import bot


channels_group = discord.SlashCommandGroup(
    name='каналы',
    description='Группа подкоманд для управления каналами франшизы'
)

@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@channels_group.command(name='добавить',
        description='Добавить новый канал в существующую франшизу')
@discord.commands.option('канал', discord.TextChannel, required=True, parameter_name='discord_channel',
        description='Выберите канал, который вы хотите удалить из франшизы')
@discord.commands.option('франшиза', str, required=True,
        parameter_name='franchise_name', autocomplete=get_franchises,
        description='Выберите существующую франшизу, в которую вы хотите добавить канал')
@discord.commands.option('тип', str, required=True,
        parameter_name='channel_type',choices=['MANAGEMENT', 'TECHNICAL'],
        description='Выберите тип канала, который вы хотите добавить в франшизу')
async def franchises_add_channel(
        ctx: discord.ApplicationContext,
        discord_channel: discord.TextChannel,
        franchise_name,
        channel_type):
    franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()
    db.query(Channel).filter(
        Channel.id == discord_channel.id
    ).delete()
    
    channel = Channel(id=discord_channel.id, franchise=franchise, type=channel_type)
    db.add(channel)
    db.commit()

    await ctx.respond(
        f'✅ Канал {discord_channel.name} успешно добавлен в франшизу {franchise.name}',
        ephemeral=True
    )


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@channels_group.command(name='удалить', description='Удалить существующий канал из франшизы')
@discord.commands.option('канал', discord.TextChannel,
        description='Выберите канал, который вы хотите удалить из франшизы',
        required=True, parameter_name='discord_channel')
@discord.commands.option('удалить-канал', bool, description='Удалить канал с сервера',
        required=True, parameter_name='delete_channel', choices=['True', 'False'])
async def franchises_remove_channel(
        ctx: discord.ApplicationContext,
        discord_channel: discord.TextChannel,
        delete_channel):

    channel = db.query(Channel).filter(
        Channel.id == discord_channel.id,
    ).first()

    if channel:
        discord_channel = bot.get_channel(channel.id)

        if delete_channel:
            await discord_channel.delete(reason='Команда /франшизы каналы удалить')

        db.delete(channel)
        db.commit()

    await ctx.respond(
        f'✅ Канал {discord_channel.name} успешно удалён',
        ephemeral=True
    )


def setup(group: discord.SlashCommandGroup):
    channels_group.parent = group
    group.add_command(channels_group)