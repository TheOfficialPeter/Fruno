import discord
from discord import Embed, Color

def generate_embed_players(gameName):
    try:
        embed = Embed(
            title="Player Statistics for " + gameName or " **[Unknown Title]**",
            description="Concurrent Players Playing the game in the past **48** hours",
            color=Color.green()
        )

        embed.set_footer(text="If you notice any sudden drops to 0, that would mean that the API was down at that point in time")
        return [True, "Successfully generated embed", embed]
    except Exception as e:
        print(f"[Error]: Failed to generate embed. Error: {e}")
        return [False, "Failed to generate embed. Please try again later.", None]