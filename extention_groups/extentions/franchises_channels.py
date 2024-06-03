import discord, config
from discord.ext import commands
from database import db, Franchise, Channel
from assets import get_free_categories
from bot import bot


channels_group = discord.SlashCommandGroup(
    name='каналы',
    description='Группа подкоманд для управления каналами франшизы'
)


def get_franchises(ctx: discord.AutocompleteContext):
    return [i.name for i in db.query(Franchise).all() if i.name.startswith(ctx.value.lower())]


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@channels_group.command(name='добавить', description='Добавить новый канал в существующую франшизу')
@discord.commands.option('канал', discord.TextChannel,
        description='Выберите канал, который вы хотите удалить из франшизы',
        required=True, parameter_name='channel')
@discord.commands.option('франшиза', str,
        description='Выберите существующую франшизу, в которую вы хотите добавить канал',
        required=True, parameter_name='franchise_name', autocomplete=get_franchises)
@discord.commands.option('тип', str,
        description='Выберите тип канала, который вы хотите добавить в франшизу',
        required=True, parameter_name='channel_type', choices=['MANAGEMENT', 'TECHNICAL'])
async def franchises_add_channel(
        ctx: discord.ApplicationContext,
        discord_channel: discord.TextChannel,
        franchise_name,
        channel_type):
    franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()
    db.query(Channel).filter(
        Channel.id == discord_channel.id
    ).delete()
    
    category = await get_free_categories([f'{channel_type} {franchise.region}'])
    await discord_channel.edit(category=category[0])
    channel = Channel(id=discord_channel.id, type=channel_type)
    franchise.channels.append(channel)
    db.commit()

    await ctx.respond(
        f'✅ Канал {discord_channel.name} успешно добавлен в франшизу {franchise.name}',
        ephemeral=True
    )


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@channels_group.command(name='удалить', description='Удалить существующий канал из франшизы')
@discord.commands.option('канал', discord.TextChannel,
        description='Выберите канал, который вы хотите удалить из франшизы',
        required=True, parameter_name='channel')
@discord.commands.option('удалить-канал', bool, description='Удалить канал с сервера',
        required=True, parameter_name='delete_channel', choices=['True', 'False'])
async def franchises_add_channel(
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