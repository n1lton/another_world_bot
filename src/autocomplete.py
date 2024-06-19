from database import db
from models.Channel import Channel
from models.Franchise import Franchise
from models.Group import Group
from bot import bot


import discord
from sqlalchemy import not_

from models.User import User


def get_free_groups(ctx: discord.AutocompleteContext):
    channel = db.query(Channel).filter(Channel.id == ctx.options['канал']).first()
    groups = db.query(Group).filter(not_(Group.channels.contains(channel))).all()

    return [
        i.name for i in groups \
        if i.name.lower().startswith(ctx.value.lower())
    ]


def get_groups(ctx: discord.AutocompleteContext):
    return [i.name for i in db.query(Group).all() if i.name.lower().startswith(ctx.value.lower())]


def get_franchises_by_user(ctx: discord.AutocompleteContext):
    discord_user = ctx.options['пользователь']
    user = db.query(User).filter(User.id == discord_user).first()
    return [
        i.name for i in db.query(Franchise).filter(Franchise.users.contains(user)).all() \
        if i.name.lower().startswith(ctx.value.lower())
    ]


def get_franchises(ctx: discord.AutocompleteContext):
    return [i.name for i in db.query(Franchise).all() if i.name.lower().startswith(ctx.value.lower())]


def get_occupied_channels(ctx: discord.AutocompleteContext):
    channels = db.query(Channel).all()

    result = []
    for channel in channels:
        discord_channel = bot.get_channel(channel.id)
        if discord_channel.name.lower().startswith(ctx.value.lower()):
            result.append(
                discord.OptionChoice(
                    name=f'{discord_channel.name} {channel.type}',
                    value=str(channel.id)
                )
            )
            
    return result


def get_channels_by_group(ctx: discord.AutocompleteContext):
    group_name = ctx.options['название-группы']
    group = db.query(Group).filter(Group.name == group_name).first()

    result = []
    for channel in group.channels:
        discord_channel = bot.get_channel(channel.id)

        if discord_channel.name.lower().startswith(ctx.value.lower()):
            result.append(
                discord.OptionChoice(
                    name=f'{discord_channel.name} {channel.type}',
                    value=str(channel.id)
                )
            )

    return result
