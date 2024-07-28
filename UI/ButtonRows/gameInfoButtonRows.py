from discord import ui, ButtonStyle
from UI.Embeds.similarGamesEmbed import generate_embed_games
from UI.Embeds.gameAnalyticsEmbed import generate_embed_players
from Logic.Fetch.fetchPlayerAnalytics import fetch_player_stats
from Logic.Fetch.fetchSimilarGames import fetch_similar_games
from Logic.Display.chartsPlayerAnalytics import convert_data_to_image_player

class embed_buttons_view(ui.View):
    def __init__(self, ctx, gameId, gameName):
        super().__init__()
        self.ctx = ctx
        self.gameId = gameId
        self.gameName = gameName
    
    @ui.button(label="View Player Analytics", style=ButtonStyle.green, emoji="📈")
    async def analytics_callback(self, button, interaction):
        # await interaction.response.send_message("Pick the type of Analytics you would like to view:", view=AnalyticsSelectMenu(self.ctx, self.title, self.gameId))
        await interaction.response.defer()

        success, message, embedData = fetch_player_stats(self.gameId)

        if not success:
            await self.ctx.followup.send(message)

        success, message, newEmbed = generate_embed_players(self.gameName)

        if not success:
            await self.ctx.followup.send(message)

        success, message, embed, chartsData = convert_data_to_image_player([newEmbed, embedData])

        if not success:
            await self.ctx.followup.send(message)
        
        await self.ctx.followup.send(embed=embed, file=chartsData)
        
    # Add some logic behind this and use Is There Any Deal
    @ui.button(label="View Similar Games", style=ButtonStyle.green, emoji="🔗")
    async def similar_games_callback(self, button, interaction):
        await interaction.response.defer()

        success, message, embedData = fetch_similar_games(self.gameId)

        if not success:
            await self.ctx.followup.send(message)

        success, message, embed = generate_embed_games(self.ctx, embedData, self.gameName)

        if not success:
            await self.ctx.followup.send(message)

        await self.ctx.followup.send(embed=embed)
