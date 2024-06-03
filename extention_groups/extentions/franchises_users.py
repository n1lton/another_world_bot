import discord, config
from discord.ext import commands
from database import db, Franchise, Channel, User
from assets import get_franchises
from bot import bot


users_group = discord.SlashCommandGroup(
    name='пользователи',
    description='Группа подкоманд для управления пользователями франшизы'
)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@users_group.command(
        name='добавить',
        description='Добавить нового пользователя в существующую франшизу')
@discord.option('пользователь', discord.Member, required=True, parameter_name='user',
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
async def users_add(ctx: discord.ApplicationContext, user: discord.Member,
        franchise_name: str, lang: str, technical: bool, management: bool):
    franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()
    franchise.users.append(User(id=user.id))

    role = bot.get_guild(config.SERVER_ID).get_role(config.ROLES[lang]['lang_role'])
    await user.add_roles(role)

    for channel in franchise.channels:
        if (channel.type == 'MANAGEMENT' and management) or (channel.type == 'TECHNICAL' and technical):
            discord_channel =  bot.get_channel(channel.id)
            await discord_channel.set_permissions(
                user,
                overwrite=discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    attach_files=True,
                    embed_links=True
                )
            )
    db.commit()






def setup(group: discord.SlashCommandGroup):
    users_group.parent = group
    group.add_command(users_group)