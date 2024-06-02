import discord, config, json
from database import cur
from discord.ext import commands
from assets import get_free_categories
from bot import bot


with open('accepted_roles.json', 'r', encoding='utf-8') as f:
        accepted_roles = json.load(f)


@commands.has_role(config.CAN_USE_BOT_ROLE_ID)
@commands.slash_command(name='добавить', description='Добавить новую франшизу')
@discord.commands.option('город', str, description='Напишите название города франшизы',
        required=True, parameter_name='city_name')
@discord.commands.option('регион-снг', bool,
        description='Установите значение True для региона СНГ или False для остального мира',
        required=True, parameter_name='is_cis', choices=['True', 'False'])
@discord.commands.option('каналы', str,
        description='Установите значение True, если необходимо создать стандартные каналы (менеджемент и технический)',
        required=True, parameter_name='create_channels', choices=['True', 'False'])
async def add_franchise(
        ctx: discord.ApplicationContext,
        city_name,
        is_cis,
        create_channels):
    cur.execute(f'SELECT name FROM franchises WHERE name = (?)', (city_name,))
    if cur.fetchone():
          await ctx.respond('❌ Франшиза с таким именем уже существует', ephemeral=True)
          return
    
    channel_ids = [-1, -1]

    if create_channels:
        guild: discord.Guild = bot.get_guild(config.SERVER_ID)

        if len(guild.channels) > 500 - 2:
              await ctx.respond('❌ Достикнуто максимальное количество каналов на сервере', ephemeral=True)
              return
        
        region = ['EN', 'RU'][is_cis]
        names = [f'TECHNICAL {region}', f'MANAGEMENT {region}']
        categories = await get_free_categories(names)

        for index, (category, name) in enumerate(zip(categories, ['TECHNICAL', 'MANAGEMENT'])):
                overwrites = {
                        guild.get_role(i): discord.PermissionOverwrite(
                                view_channel=True, send_messages=True
                        ) for i in accepted_roles[region][name]
                }
                overwrites[guild.default_role] = discord.PermissionOverwrite(view_channel=False)
                
                channel = await guild.create_text_channel(
                        name=city_name,
                        overwrites=overwrites,
                        category=category
                )

                channel_ids[index] = channel.id
        
        cur.execute(f'INSERT INTO franchises VALUES (?, ?, ?)', (city_name, *channel_ids))
        await ctx.respond('✅ Франшиза создана', ephemeral=True)


def setup(group: discord.SlashCommandGroup):
      add_franchise.parent = group
      group.add_command(add_franchise)