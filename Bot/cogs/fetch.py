from discord.ext import commands
from discord import Embed, Color, ui, ButtonStyle
from datetime import date
import requests
from buttonRows.mainButtonRow import ButtonRow   

class FetchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="fetch")
    async def fetch(self, ctx, game: str):
        self.interaction = ctx
        
        if "Buyer" in [role.name for role in ctx.author.roles] and game != "":
            resp = requests.get(f"https://6651005cb09f1b83aa75.appwrite.global/fetch?name={game}", timeout=50)

            if resp.ok:
                resp = resp.json()

                try:
                    embed = Embed(
                        title="Game Information",
                        description=date.today(),
                        color=Color.green()
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
                            resp['desc'] = ' (Invalid ProtonDB tier)'

                    embed.add_field(name="Linux Compatibility Tier", value=resp['tier'] + resp['desc'], inline=False)
                    embed.add_field(name="Linux Compatibility Tier Score", value=resp['tierScore'], inline=False)
                    embed.set_image(url=resp['image'])

                    await self.interaction.respond(embed=embed, view=ButtonRow())
                except:
                    await self.interaction.respond("Game was found, but information could not be gathered correctly. Please try again later or wait for update")
            else:
                await self.interaction.respond("Something went wrong with the API. Please try again later or wait for update")
        else:
            await self.interaction.respond("You do not have the required '@Buyer' role.")

def setup(bot):
    bot.add_cog(FetchCommand(bot))
