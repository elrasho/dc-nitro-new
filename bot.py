# bot file
import os
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='@(!*@(')
cfg_file = open('config.json', 'r', encoding="UTF-8").read()
cfg = json.loads(cfg_file)
# I am assuming that you have a test.py cog in a cogs folder
# bot.load_extension('cogs.test') # this is good but you can make it better

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
    
  else:
    print(f'Unable to load {filename[:-3]}')
    
bot.run(cfg['user']['bot_token'])