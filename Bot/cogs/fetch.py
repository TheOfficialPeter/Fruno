from discord.ext import commands
from discord import Embed, Color, ui, ButtonStyle, EmbedMedia
from datetime import date
import requests
from functions.playerStats import *
#from functions.recommend import *

class ButtonRow(ui.View):
    def __init__(self, gameId, title, ctx):
        super().__init__()
        self.ctx = ctx
        self.gameId = gameId
        self.title = title

    @ui.button(label="View Analytics", style=ButtonStyle.green, emoji="📈")
    async def analytics_callback(self, button, interaction):
        await interaction.response.defer()

        result = fetchPlayerStats(self.gameId)

        if result[0]:
            embed = Embed(
                title="Player Statistics for " + self.title or " [Unknown Title]",
                description="Concurrent Players Playing the game in the past **48** hours",
                color=Color.green()
            )

            result = convertDataToImage(result[2], embed)
             
            if result is None:
                await self.ctx.followup.send(embed=result[0], file=result[1])
            else:
                await self.ctx.followup.send(f"There was a problem fetching the Player Analytics for {self.title}. Please report this and wait for an update from the developer. Sorry for the inconvenience")
        else:
            await self.ctx.followup.send(result[1])

    @ui.button(label="Recommendations", style=ButtonStyle.green, emoji="♻️")
    async def recommendation_callback(self, button, interaction):
        #recommendedResponse = getRecommendedGames(self.title)

        #if recommendedResponse != "":
            # use the recommended games string
            #await self.ctx.followup.send(recommendedResponse)
        #else:
            #await self.ctx.followup.send("Could not get recommended games")
        await self.ctx.followup.send("Could not get recommended games")

    @ui.button(label="Installation", style=ButtonStyle.green, emoji="⚒️")
    async def installation_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")  

    @ui.button(label="Downloads", style=ButtonStyle.green, emoji="⬇️")
    async def downloads_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")

class FetchCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="fetch")
    async def fetch(self, ctx, game: str):
        await ctx.interaction.response.defer()

        if "Buyer" in [role.name for role in ctx.author.roles] and game != "":
            resp = requests.get(f"https://6651005cb09f1b83aa75.appwrite.global?name={game}", timeout=50)
            
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
                            resp['desc'] = ' (Invalid ProtonDB tier)'

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
            await ctx.interaction.respond("You do not have the required '@Buyer' role.")

def setup(bot):
    bot.add_cog(FetchCommand(bot))
