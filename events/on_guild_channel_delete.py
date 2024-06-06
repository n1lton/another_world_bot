import discord
from database import db
from models.Channel import Channel

async def on_guild_channel_delete(discord_channel: discord.abc.GuildChannel):
    if isinstance(discord_channel, discord.TextChannel):
        db.query(Channel).filter(
            Channel.id == discord_channel.id
        ).delete()
        db.commit()


def setup(bot):
    bot.event(on_guild_channel_delete)