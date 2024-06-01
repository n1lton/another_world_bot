import config, os
from bot import bot
from database import cur

cur.execute('''
    CREATE TABLE IF NOT EXISTS categories
''')
for i in os.listdir('extentions_groups'):
    if i.endswith('.py'):
        bot.load_extension(f'extentions_groups.{i.removesuffix('.py')}')

bot.run(config.TOKEN)