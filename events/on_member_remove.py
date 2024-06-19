import discord
from database import db
from models.User import User


async def on_member_remove(member: discord.Member):
    user = db.query(User).filter(
        User.id == member.id
    ).first()
    if user:
        db.delete(user)
        db.commit()


def setup(bot):
    bot.event(on_member_remove)