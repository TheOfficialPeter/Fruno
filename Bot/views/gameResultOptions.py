from discord import ui, ButtonStyle
from views.analyticsSelectMenu import AnalyticsSelectMenu

class OptionsRow(ui.View):
    """
    Class for display a row of options for fetched game responses. It allows you to easily 
    manage additional results or expanded information on the game

    Keyword arguments:
    gameId: String containing the steam ID of the game
    title: Describe the title label for the select menu
    ctx: The discord interaction embed object
    returns: N/A
    """ 

    def __init__(self, gameId, title, ctx):
        super().__init__()
        self.ctx = ctx
        self.gameId = gameId
        self.title = title

    @ui.button(label="View Analytics", style=ButtonStyle.green, emoji="📈")
    async def analytics_callback(self, button, interaction):
        await interaction.response.send_message("Pick the type of Analytics you would like to view:", view=AnalyticsSelectMenu(self.ctx, self.title, self.gameId))