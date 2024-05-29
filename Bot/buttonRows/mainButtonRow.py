from discord import ui, ButtonStyle

class ButtonRow(ui.View):
    @ui.button(label="View Analytics", style=ButtonStyle.green, emoji="📈")
    async def analytics_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")

    @ui.button(label="Recommendations", style=ButtonStyle.green, emoji="♻️")
    async def recommendation_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")

    @ui.button(label="Installation", style=ButtonStyle.green, emoji="⚒️")
    async def installation_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")  

    @ui.button(label="Downloads", style=ButtonStyle.green, emoji="⬇️")
    async def downloads_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")