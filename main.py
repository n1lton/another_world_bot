import config, os
from bot import bot
from database import cur

cur.execute('''
    CREATE TABLE IF NOT EXISTS franchises (
        name STRING PRIMATY KEY,
        technical_channel_id INTEGER,
        management_channel_id INTEGER
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS partners (
        id INTEGER,
        franchise_name STRING PRIMARY KEY
    )
''')

for i in os.listdir('extentions_groups'):
    if i.endswith('.py'):
        name = i.removesuffix('.py')
        print(f'Loading extention {name}...')
        bot.load_extension(f'extentions_groups.{name}')
        

for i in os.listdir('events'):
    if i.endswith('.py'):
        name = i.removesuffix('.py')
        print(f'Loading event {name}...')
        bot.load_extension(f'events.{i.removesuffix('.py')}')

bot.run(config.TOKEN)