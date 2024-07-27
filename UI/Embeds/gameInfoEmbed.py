from discord import Embed, Color
from datetime import datetime
from UI.ButtonRows.gameInfoButtonRows import embed_buttons_view

def generate_embed(ctx, embedData):
    try:
        embed = Embed(
            title="Game Information",
            color=Color.green(),
            timestamp=datetime.now()
        )

        embed.add_field(name="Title", value=embedData['title'], inline=False)
        embed.add_field(name="Game ID", value=embedData['gameId'], inline=False)

        embed.add_field(name="Linux Compatibility Tier", value=embedData['tier'] + embedData['desc'], inline=False)
        embed.add_field(name="Peak Player Count", value=str(embedData['ccu']), inline=False)
        embed.add_field(name="Youtube Video Uploads Recently", value=str(embedData['yt']), inline=False)
        embed.add_field(name="Current Price", value=str(embedData['price']), inline=False)
        embed.set_image(url=embedData['image'])
        
        return [True, "Successfully generated embed.", embed, embed_buttons_view(ctx, embedData['gameId'], embedData['title'])]
    except Exception as e:
        print("[Error] Failed to generate embed: " + str(e))
        return [False, "Failed to fetch game information.", None]