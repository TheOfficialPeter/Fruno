from discord.ext import commands
from discord import Embed, Color
import datetime
import requests
from config import API_URI
from enums.enums import Role
from views.gameResultOptions import OptionsRow

class FetchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="fetch")
    async def fetch(self, ctx, game: str):
        await ctx.interaction.response.defer()

        if Role.BUYER.value in [role.name for role in ctx.author.roles] and game != "":
            resp = requests.get(API_URI + game, timeout=50)
            
            if resp.ok:
                try:
                    resp = resp.json()
                    
                    embed = Embed(
                        title="Game Information",
                        color=Color.green(),
                        timestamp=datetime.now()
                    )

                    embed.add_field(name="Title", value=resp['title'], inline=False)
                    embed.add_field(name="Game ID", value=resp['gameId'], inline=False)

                    match resp['tier'].lower():
                        case "bronze":
                            resp['desc'] = ' (Game has significant compatibility issues on Linux with Proton)'
                        case "silver":
                            resp['desc'] = ' (Game has minor compatibility problems on Linux with Proton)'
                        case "gold":
                            resp['desc'] = ' (Game runs very well on Linux with Proton)'
                        case "platinum":
                            resp['desc'] = ' (Game runs flawlessly on Linux with Proton)'
                        case "borked":
                            resp['desc'] = ' (Game is completely broken and unplayable on Linux with Proton)'
                        case _:
                            resp['desc'] = ' (Invalid ProtonDB tier. Linux game compatibility is unknown)'

                    embed.add_field(name="Linux Compatibility Tier", value=resp['tier'] + resp['desc'], inline=False)
                    embed.add_field(name="Peak Player Count", value=str(resp['ccu']), inline=False)
                    embed.add_field(name="Youtube Video Uploads Recently", value=str(resp['yt']), inline=False)
                    embed.add_field(name="Current Price", value=str(resp['price']), inline=False)
                    embed.set_image(url=resp['image'])

                    await ctx.followup.send(embed=embed, view=ButtonRow(resp['gameId'], resp['title'], ctx))
                except Exception as e:
                    await ctx.followup.send("Something went wrong: " + resp.text or e)
            else:
                await ctx.followup.send("Something went wrong with the API. Please try again later or wait for update")
        else:
            await ctx.interaction.respond("You do not have the required 'Buyer' role.")

def setup(bot):
    bot.add_cog(FetchCommand(bot))
