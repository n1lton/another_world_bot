import discord, config
from discord.ext import commands
from database import db
from models.User import User
from models.Franchise import Franchise
from models.Channel import Channel

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.all(),
    debug_guilds=[1190218751015125033]
)

@bot.event
async def on_ready():
    print('Bot is running.')

    guild = bot.get_guild(1190218751015125033)

    for discord_channel in guild.text_channels:
        if discord_channel.name.lower() in ('👁another-world', 'канал-с-обновлениями', 'updates-channel', 'aw_partners_test', '🎮техподдержка', 'bot-channel'):
            continue
        
        franchise_name = discord_channel.name.capitalize()
        channel_type = 'MANAGEMENT' if discord_channel.category.name.lower().startswith('management') else 'TECHNICAL'

        channel = Channel(id=discord_channel.id, type=channel_type)

        franchise = db.query(Franchise).filter(Franchise.name == franchise_name).first()
        if not franchise:
            franchise = Franchise(name=franchise_name)
            db.add(franchise)

        franchise.channels.append(channel)

        for i in discord_channel.overwrites.keys():
            if not isinstance(i, discord.Member):
                continue

            if i.id not in [x.id for x in franchise.users]:
                user = db.query(User).filter(User.id == i.id).first()
                if user and user in franchise.users:
                    continue

                if not user:
                    user = User(id=i.id)

                franchise.users.append(user)

    db.commit()
    print('Парсинг завершен.')


bot.run(config.TOKEN)