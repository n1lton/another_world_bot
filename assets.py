import discord, config
from bot import bot


async def get_free_categories(names: list[str]) -> list[discord.CategoryChannel]:
    result = []
    for name in names:
        category = await get_free_category(name)
        result.append(category)

    return tuple(result)


async def get_free_category(name: str):
    guild: discord.Guild = bot.get_guild(config.SERVER_ID)
    count = 0
    result = None

    for category in guild.categories:
        if not category.name.lower().startswith(name.lower()):
            continue

        count += 1

        if len(category.channels) < config.MAX_CHANNELS:
            result = category
            break

    if result == None:
        result = await guild.create_category(
            name=f'{name}{" " + str(count + 1) if count != 0 else ""}',
            position=get_max_position(name)
        )

    return result
            

def get_max_position(name: str):
    guild: discord.Guild = bot.get_guild(config.SERVER_ID)
    return max(
        [
            category.position for category in guild.categories \
            if category.name.lower().startswith(name.lower())
        ]
    )
