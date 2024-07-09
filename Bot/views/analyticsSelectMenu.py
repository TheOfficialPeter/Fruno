import discord
from discord import Embed, Color
from extra.playerStats import *
from extra.twitchStats import *

"""
File Info:
File contains a View for a Discord Select Menu template which is currently used for different game analytics
"""

class AnalyticsSelectMenu(discord.ui.View):
    """
    Analytics Menu Class to show different types of statistics pages for specified games.
    Provide information to build the select menu and functionality for the Analytics Select Menu component.
    Easy to implement into the rest of the codebase.

    Optional keyword arguments:
    title: Describe the title label for the select menu
    options: Dictionary containing Key and Value params for describing each option in the select menu.
    return: Returns the selected item from the select menu for further processing.
    """ 

    def __init__(self, ctx, title, gameId):
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
            discord.SelectOption(
                label="Twitch Analytics",
                description="Fetches the latest Twitch Viewer Analytics for the game",
                value="twitch"
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

                    result = convertDataToImage_Player(result[2], embed)
                    
                    if result[0]:
                        await self.ctx.followup.send(embed=result[0], file=result[1])
                    else:
                        await self.ctx.followup.send(f"There was a problem fetching the Player Analytics for {self.title}. Please report this and wait for an update from the developer. Sorry for the inconvenience")
                else:
                    await self.ctx.followup.send(result[1])
                        
            # Fetch Twitch Analytics
            case "twitch":
                result = fetchTwitchStats(self.gameId)
                
                if result[0]:
                    embed = Embed(
                        title="Twitch Viewer Statistics for " + self.title or " **[Unknown Title]**",
                        description="Twitch Viewers watching the game in the past **48** hours",
                        color=Color.green()
                    )

                    result = convertDataToImage_Twitch(result[2], embed)
                    
                    if result[0]:
                        await self.ctx.followup.send(embed=result[0], file=result[1])
                    else:
                        await self.ctx.followup.send(f"There was a problem fetching the Twitch Analytics for {self.title}. Please report this and wait for an update from the developer. Sorry for the inconvenience")
                else:
                    await self.ctx.followup.send(result[1])

            # Fetch Pricing Analytics
            case "price":
                pass

        return select.values[0]