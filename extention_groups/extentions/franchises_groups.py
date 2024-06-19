from autocomplete import get_free_groups, get_occupied_channels, get_groups, get_channels_by_group
import discord, config
from discord.ext import commands
from database import db
from models.Group import Group
from models.User import User
from models.Channel import Channel
from bot import bot


users_group = discord.SlashCommandGroup(
    name='группы',
    description='Группа подкомманд для управления группами пользователей'
)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(name='создать', description='Создать новую пользовательскую группу')
@discord.commands.option('название-группы', str, required=True, parameter_name='group_name',
        description='Введите название для новой группы')
async def create_group(ctx: discord.ApplicationContext, group_name: str):
    group = db.query(Group).filter(Group.name == group_name).first()
    if group:
        await ctx.respond('❌ Группа с таким именем уже существует', ephemeral=True)
        return
    
    group = Group(name=group_name)
    db.add(group)
    db.commit()

    await ctx.respond(f'✅ Группа {group_name} создана', ephemeral=True)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(name='удалить', description='Удалить существующую группу пользователей')
@discord.commands.option('название-группы', str, required=True,
        parameter_name='group_name', autocomplete=get_groups,
        description='Введите название удаляемой группы')
async def delete_group(ctx: discord.ApplicationContext, group_name: str):
    group = db.query(Group).filter(Group.name == group_name).first()
    if not group:
        await ctx.respond('❌ Группа не найдена', ephemeral=True)
        return
    
    db.delete(group)
    await ctx.respond(f'✅ Группа {group_name} удалена', ephemeral=True)
    db.commit()


def get_text(groups, mention=False):
    text = ''
    
    for group in groups:
        text += f'Группа {group.name}:\n'

        discord_channels = []
        for channel in group.channels:
            discord_channels.append(bot.get_channel(channel.id))

        for discord_channel in sorted(discord_channels, key=lambda a: a.name[0]):
            discord_channel: discord.TextChannel
            category_name = f' ({discord_channel.category.name})' if discord_channel.category else ''
            if mention:
                text += f'- <#{discord_channel.id}>{category_name}\n'
            else:
                text += f'- {discord_channel.name}{category_name} id: {channel.id}\n'

        if not group.channels:
            text += '- Каналы отсутствуют\n'

        text += '\n'

    if not groups:
        text = 'Группы отсутствуют'

    return text


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(name='список', description='Вывести список групп и их каналы')
async def print_groups(ctx: discord.ApplicationContext):
    groups = db.query(Group).all()
    text = get_text(groups, mention=True)

    if len(text) > 2000:
        with open('buffer.txt', 'w', encoding='utf-8') as f:
            f.write(get_text(groups, mention=False))
        
        await ctx.respond(file=discord.File('buffer.txt'), ephemeral=True)

    else:
        await ctx.respond(text, ephemeral=True)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(name='добавить-канал', description='Добавить канал в группу')
@discord.commands.option('канал', str, required=True,
        parameter_name='channel_id', autocomplete=get_occupied_channels,
        description='Выберите канал')
@discord.commands.option('название-группы', str, required=True,
        parameter_name='group_name', autocomplete=get_free_groups,
        description='Введите название группы, в которую необходимо добавить канал')
async def add_channel_to_group(ctx: discord.ApplicationContext, channel_id: str, group_name: str):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    group = db.query(Group).filter(Group.name == group_name).first()

    if not channel or not group:
        await ctx.respond('❌ Канал или группа не найдены', ephemeral=True)
        return
    
    group.channels.append(channel)
    db.commit()

    await ctx.respond('✅ Канал добавлен в группу', ephemeral=True)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(name='удалить-канал', description='Удалить выбранный канал из выбранной группы')
@discord.commands.option('название-группы', str, required=True,
        parameter_name='group_name', autocomplete=get_groups,
        description='Введите название группы, из которой необходимо удалить канал')
@discord.commands.option('канал', str, required=True,
        parameter_name='channel_id', autocomplete=get_channels_by_group,
        description='Выберите канал')
async def delete_channel_from_group(ctx: discord.ApplicationContext, group_name: str, channel_id: str):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    group = db.query(Group).filter(Group.name == group_name).first()
    
    if not channel or not group:
        await ctx.respond('❌ Канал или группа не найдены', ephemeral=True)
        return
    
    group.channels.remove(channel)
    db.commit()

    await ctx.respond('✅ Канал удалён из группы', ephemeral=True)


def setup(category: discord.SlashCommandGroup):
    users_group.parent = category
    category.add_command(users_group)
