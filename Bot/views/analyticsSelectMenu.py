import discord
from discord import Embed, Color
from extra.stats.playerStats import *

"""
File Info:
File contains a View for a Discord Select Menu template which is currently used for different game analytics
"""

class AnalyticsSelectMenu(discord.ui.View):

    def __init__(self, ctx, title, gameId):
        """
        Initializes the AnalyticsSelectMenu class with the provided context, title, and gameId.

        Parameters:
            ctx (discord.Context): The context object for the menu.
            title (str): The title label for the select menu.
            gameId (str): The ID of the game.

        Returns:
            None
        """
        super().__init__()
        self.title = title
        self.ctx = ctx
        self.gameId = gameId
    
    @discord.ui.select(
        placeholder = "Pick type of Analytics",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Player Analytics (2 days)",
                description="Get Concurrent Playing on this game for the past 48 hours",
                value="player"
            ),
            # This option might be a paid plan. So put it outside at some point
            discord.SelectOption(
                label="Pricing Analytics",
                description="Fetches the pricing analytics over the course of time for easy comparison",
                value="price"
            )
        ]
    )

    async def analytics_select_menu_callback(self, select, interaction):
        await interaction.response.defer()
        await interaction.message.delete()
        
        match select.values[0]:
            # Fetch Player Analytics
            case "player":
                result = fetchPlayerStats(self.gameId)

                if result[0]:
                    embed = Embed(
                        title="Player Statistics for " + self.title or " **[Unknown Title]**",
                        description="Concurrent Players Playing the game in the past **48** hours",
                        color=Color.green()
                    )

                    embed.set_footer(text="If you notice any sudden drops to 0, that would mean that the API was down at that point in time")

                    result = convert_data_to_image_player(result[2], embed)
                    
                    if result[0]:
                        await self.ctx.followup.send(embed=result[0], file=result[1])
                    else:
                        await self.ctx.followup.send(f"There was a problem fetching the Player Analytics for {self.title}. Please report this and wait for an update from the developer. Sorry for the inconvenience")
                else:
                    await self.ctx.followup.send(result[1])
                        
            # Fetch Pricing Analytics
            case "price":
                await self.ctx.followup.send("Yep still working on this one. Should be out once I finish up my custom scraper")

        return select.values[0]
