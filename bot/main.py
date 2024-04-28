import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from fetch_cog import FetchCommand

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

if __name__ == "__main__":
    print("Adding FetchCommand Cog to the bot...")
    bot.add_cog(FetchCommand(bot))
    print("FetchCommand Cog added to the bot.")
    bot.run(TOKEN)
