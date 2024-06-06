import discord
from database import db
from models.User import User


async def on_member_remove(member: discord.Member):
    db.query(User).filter(
        User.id == member.id
    ).delete()
    db.commit()


def setup(bot):
    bot.event(on_member_remove)