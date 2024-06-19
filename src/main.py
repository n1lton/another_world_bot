import config, os
from bot import bot

for i in os.listdir('extention_groups'):
    if i.endswith('.py'):
        name = i.removesuffix('.py')
        print(f'Loading extention {name}...')
        bot.load_extension(f'extention_groups.{name}')
        

for i in os.listdir('events'):
    if i.endswith('.py'):
        name = i.removesuffix('.py')
        print(f'Loading event {name}...')
        bot.load_extension(f'events.{i.removesuffix('.py')}')

bot.run(config.TOKEN)