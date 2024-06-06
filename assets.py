import discord, config
from bot import bot


async def get_free_categories(names: list[str]) -> list[discord.CategoryChannel]:
    guild: discord.Guild = bot.get_guild(config.SERVER_ID)
    result = {i: None for i in names}
    categories_count = {i: 0 for i in names}

    for category in guild.categories:
        names_mask = [category.name.lower().startswith(i.lower()) for i in names]
        if not any(names_mask):
            continue

        name = names[names_mask.index(True)]
        
        if len(category.channels) < config.MAX_CHANNELS:
            result[name] = category

        categories_count[name] += 1

    for k, v in result.items():
        if v == None:
            result[k] = await guild.create_category(
                name=f'{k} {categories_count[k] + 1}'
            )

    return tuple(result[name] for name in names)
