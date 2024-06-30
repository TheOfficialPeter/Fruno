from discord import Embed, Color, ui, ButtonStyle
from extra.playerStats import *

class OptionsRow(ui.View):
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
             
            if result:
                await self.ctx.followup.send(embed=result[0], file=result[1])
            else:
                await self.ctx.followup.send(f"There was a problem fetching the Player Analytics for {self.title}. Please report this and wait for an update from the developer. Sorry for the inconvenience")
        else:
            await self.ctx.followup.send(result[1])