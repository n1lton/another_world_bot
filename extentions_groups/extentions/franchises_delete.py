import discord, config
from discord.ext import commands
from database import cur
from bot import bot


def get_cities(ctx: discord.AutocompleteContext):
    data = cur.execute('SELECT name FROM franchises').fetchall()
    return [i[0] for i in data if i[0].startswith(ctx.value.lower())]

@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='удалить', description='Удалить существующую франшизу')
@discord.commands.option('найти-город', str,
        description='Напишите название города франшизы для поиска',
        required=True, parameter_name='city_name', autocomplete=get_cities)
@discord.commands.option('удалить-с-сервера', str,
        description='Установите значение True, если необходимо удалить партнёра с сервера',
        required=True, parameter_name='delete_partner', choices=['True', 'False'])
async def delete_franchise(ctx: discord.ApplicationContext, city_name, delete_partner):
    guild = bot.get_guild(config.SERVER_ID)

    if delete_partner:
        cur.execute('SELECT id FROM partners WHERE franchise_name = (?)', (city_name,))
        data = cur.fetchone()
        if data:
            member = guild.get_member(data[0])
            await member.ban(reason=f'Удаление франшизы {city_name}')
            cur.execute('DELETE FROM partners WHERE franchise_name = (?)', (city_name,))

    cur.execute(
        'SELECT technical_channel_id, management_channel_id FROM franchises WHERE name = (?)',
        (city_name,)
    )
    channel_ids = cur.fetchone()
    for channel_id in channel_ids:
        if channel_id == -1:
            continue

        channel = guild.get_channel(channel_id)
        
        if channel.category and len(channel.category.channels) == 1:
            await channel.category.delete(reason=f'Удаление франшизы {city_name}')

        await channel.delete(reason=f'Удаление франшизы {city_name}')

    cur.execute('DELETE FROM franchises WHERE name = (?)', (city_name,))

    await ctx.respond('✅ Франшиза удалена', ephemeral=True)


def setup(group: discord.SlashCommandGroup):
      delete_franchise.parent = group
      group.add_command(delete_franchise)