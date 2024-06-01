import requests
from discord import File
from datetime import datetime
import io
import matplotlib.pyplot as plt

def fetchPlayerStats(gameId):
    if gameId != "":
        resp = requests.get(f"https://6658c2a589ac905ba57f.appwrite.global/?id={gameId}")

        if resp.ok:
            try:
                stats = resp.json()
                return [True, "Successfully fetched game player stats", stats]
            except:
                return [False, "Could not fetch game player stats. Response body invalid", None]

        else:
            return [False, "Could not fetch game player stats. Request unsuccessful", None]
    else:
        return [False, "Could not fetch game player stats. Game ID not provided", None]

def convertDataToImage(data, embed):
    if data and len(data) > 5:
        data_stream = io.BytesIO()

        time = list(map(lambda x: datetime.fromtimestamp(x[0]/1000).strftime("%H"), data))
        players = list(map(lambda x: x[1], data))

        plt.figure(figsize=(15,5))
        plt.xlabel("Time")
        plt.ylabel("Players")
        plt.plot(time, players)
        plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
        plt.close()

        data_stream.seek(0)
        chart = File(data_stream, filename="player_stats.png")

        embed.set_image(
            url="attachment://player_stats.png"
        )

        return [embed, chart]
    else:
        return [False, "Could not convert player stats data to image. Unexpected data input", None]