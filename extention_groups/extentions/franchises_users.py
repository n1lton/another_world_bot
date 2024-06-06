from models.User import User
from models.Franchise import Franchise
from autocomplete import get_franchises_by_user
import discord, config
from discord.ext import commands
from database import db
from autocomplete import get_franchises
from bot import bot


users_group = discord.SlashCommandGroup(
    name='пользователи',
    description='Группа подкоманд для управления пользователями франшизы'
)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(
        name='добавить',
        description='Добавить нового пользователя в существующую франшизу')
@discord.option('пользователь', discord.Member, required=True, parameter_name='discord_user',
        description='Выберите пользователя, которого хотите добавить во франшизу')
@discord.option('франшиза', str, required=True, parameter_name='franchise_name', autocomplete=get_franchises,
        description='Выберите существующую франшизу, в которую вы хотите добавить пользователя')
@discord.commands.option('язык', str, required=True,
        parameter_name='lang', choices=['RU', 'EN'],
        description='Выберите язык пользователя: RU или EN')
@discord.commands.option('technical', bool, required=False,
        parameter_name='technical', choices=['True', 'False'],
        description='Выберите значение true, если хотите выдать доступ к техническому каналу')
@discord.commands.option('management', bool, required=False,
        parameter_name='management', choices=['True', 'False'],
        description='Выберите значение true, если хотите выдать доступ к каналу менеджемента')
async def users_add(ctx: discord.ApplicationContext, discord_user: discord.Member,
        franchise_name: str, lang: str, technical: bool, management: bool):
    franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()

    user = db.query(User).filter(User.id == discord_user.id).first()
    if not user:
        user = User(id=discord_user.id)

    if user in franchise.users:
        await ctx.respond(
            f'❌ Пользователь {discord_user.mention} уже есть во франшизе {franchise_name}',
            ephemeral=True
        )
        return
    
    franchise.users.append(user)

    role = bot.get_guild(config.SERVER_ID).get_role(config.ROLES[lang]['lang_role'])
    if role not in discord_user.roles:
        await discord_user.add_roles(role)

    for channel in franchise.channels:
        if (channel.type == 'MANAGEMENT' and management) or (channel.type == 'TECHNICAL' and technical):
            discord_channel =  bot.get_channel(channel.id)
            await discord_channel.set_permissions(
                discord_user,
                overwrite=discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    attach_files=True,
                    embed_links=True
                )
            )

    db.commit()

    await ctx.respond(
        f'✅ Пользователь {discord_user.mention} добавлен во франшизу {franchise_name}',
        ephemeral=True
    )


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(name='удалить', description='Удалить пользователя из франшизы')
@discord.option('пользователь', discord.Member, required=True, parameter_name='discord_user',
        description='Выберите пользователя, которого хотите удалить из франшизы')
@discord.commands.option('выгнать', bool, required=True,
        parameter_name='ban', choices=['True', 'False'],
        description='Выберите значение true, если хотите выгнать партнёра с сервера')
@discord.commands.option('франшиза', str, required=True,
        parameter_name='franchise_name', autocomplete=get_franchises_by_user,
        description='Выберите франшизу, из которой необходимо удалить пользователя')
async def remove_user(ctx: discord.ApplicationContext, discord_user: discord.Member, franchise_name, ban):
    user = db.query(User).filter(User.id == discord_user.id).first()
    if not user:
        await ctx.respond('❌ Пользователь не найден', ephemeral=True)
        return
    
    if ban:
        db.delete(user)
        await discord_user.kick(reason='Команда /франшизы каналы удалить')

    else:
        franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()
        franchise.users.remove(user)
        for channel in franchise.channels:
            discord_channel = bot.get_channel(channel.id)
            await discord_channel.set_permissions(
                discord_user,
                overwrite=discord.PermissionOverwrite()
            )

    db.commit()
    await ctx.respond('✅ Пользователь удалён', ephemeral=True)


def setup(group: discord.SlashCommandGroup):
    users_group.parent = group
    group.add_command(users_group)