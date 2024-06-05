import discord, config
from discord.ext import commands
from database import db
from models.Group import Group
from models.User import User
from models.Channel import Channel
from assets import get_groups
import time


users_group = discord.SlashCommandGroup(
    name='группы',
    description='Группа подкомманд для управления группами пользователей'
)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(name='создать', descriprion='Создать новую пользовательскую группу')
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
@users_group.command(name='удалить', descriprion='Удалить существующую группу пользователей')
@discord.commands.option('название-группы', str, required=True,
        parameter_name='group_name', autocomplete=get_groups,
        description='Введите название удаляемой группы')
async def delete_group(ctx: discord.ApplicationContext, group_name: str):
    db.query(Group).filter(Group.name == group_name).delete()
    await ctx.respond(f'✅ Группа {group_name} удалена', ephemeral=True)


def get_text(groups, mention=False):
    text = ''
    
    for group in groups:
        text += f'Группа {group.name}:\n'

        for channel in group.channels:
            if mention:
                text += f'- <#{channel}>'
            else:
                text += f'- {channel.name} (id: {channel.id})\n'

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
    text = 'сво' * 2000
    if len(text) > 2000:
        with open('buffer.txt', 'w', encoding='utf-8') as f:
            f.write(get_text(groups, mention=False))
        
        await ctx.respond(file=discord.File('buffer.txt'), ephemeral=True)

    else:
        await ctx.respond(text, ephemeral=True)
    
    






def setup(category: discord.SlashCommandGroup):
    users_group.parent = category
    category.add_command(users_group)
