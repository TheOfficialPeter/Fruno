from discord.ext import commands
from discord import Embed, Color
import requests

class Cog1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="fetch")
    async def fetch(self, ctx, game: str):
        if "Buyer" in [role.name for role in ctx.author.roles] and game != "":
            # fetch game info
            resp = requests.get(f"https://6651005cb09f1b83aa75.appwrite.global/fetch?name={game}", timeout=50)
            resp = resp.json()

            embed = Embed(
                title="Game Information",
                description=f"Details for the game: {game}",
                color=Color.blue()
            )

            # Add fields to the embed
            embed.add_field(name="Title", value=resp.get('title', resp['title']), inline=False)
            embed.add_field(name="Game ID", value=resp.get('gameId', resp['gameId']), inline=False)
            embed.add_field(name="User Score", value=resp.get('userScore', resp['userScore']), inline=False)
            embed.add_field(name="Tier", value=resp.get('tier', resp['tier']), inline=False)
            embed.add_field(name="Tier Score", value=resp.get('tierScore', resp['tierScore']), inline=False)
            embed.set_image(url=resp.get('image', resp['image']))

            # Send the embed as a response
            await ctx.respond(embed=embed)
            await ctx.send(f"||{resp['trailer']}||")
        else:
            await ctx.respond("You do not have the required 'Buyer' role.")

def setup(bot):
    bot.add_cog(Cog1(bot))
