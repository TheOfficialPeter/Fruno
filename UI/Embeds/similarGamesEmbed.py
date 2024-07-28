from discord import Embed, Color
from datetime import datetime

def generate_embed_games(ctx, embedData, gameName):
    try:
        embed = Embed(
            title="Games Similar to " + gameName,
            color=Color.green(),
            timestamp=datetime.now()
        )

        for similarGameIndex in range(len(embedData)-1):
            similarGame = embedData[similarGameIndex]
        
            finalString = ""
            finalString += f"Title: {similarGame['title']}\n"
            finalString += f"Tags: {', '.join(similarGame['tags'])}\n"
            finalString += f"Likes: {similarGame['likes']}\n"
            finalString += f"Dislikes: {similarGame['dislikes']}\n"
            finalString += f"Trailer: {similarGame['trailer']}\n"

            embed.add_field(name=f"Game #{similarGameIndex+1}: {similarGame['title']}", value=finalString, inline=False)
                
        return [True, "Successfully generated embed.", embed]
    except Exception as e:
        print("[Error] Failed to generate embed: " + str(e))
        return [False, "Failed to fetch similar game information.", None]