import discord
from discord.ext import commands
import os
from config import TOKEN

intents = discord.Intents.default()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

def load_cogs(bot):
    cogs_dir = os.path.dirname(__file__) + '/Commands'
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            extension = f'Commands.{filename[:-3]}'
            
            try:
                bot.load_extension(extension)
                print(f'Successfully loaded extension {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')

load_cogs(bot)
bot.run(TOKEN)
