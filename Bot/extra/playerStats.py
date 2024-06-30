import requests
from discord import File
from datetime import datetime
import io
import matplotlib.pyplot as plt
from config import ANALYTICS_API_URI

def fetchPlayerStats(gameId):
    if gameId != "":
        resp = requests.get(ANALYTICS_API_URI + gameId)

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
        try: 
            data_stream = io.BytesIO()

            time = list(map(lambda x: datetime.utcfromtimestamp(x[0]/1000).strftime("%H"), data))
            players = list(map(lambda x: x[1], data))

            fig, ax = plt.subplots(figsize=(15,5))

            # colors 
            ax.set_facecolor('#23272A')
            ax.tick_params(axis='x', colors='white')  # X-axis tick labels and ticks
            ax.tick_params(axis='y', colors='white')  # Y-axis tick labels and ticks
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.grid(color='gray', linestyle='--', linewidth=0.5)
            fig.patch.set_facecolor('#23272A')

            plt.xlabel("Time", color='lightgreen')
            plt.ylabel("Players", color='lightgreen')
            plt.plot(time, players, color='lightgreen')
            plt.title("Player Statistics Over Time", color='lightgreen')
            plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
            plt.close()

            data_stream.seek(0)
            chart = File(data_stream, filename="player_stats.png")

            embed.set_image(
                url="attachment://player_stats.png"
            )
            
            return [embed, chart]
        except Exception as e:
            print("[Fruno Error]: Failed to generate graphs")
            return [None, None]

    else:
        return [False, "Could not convert player stats data to image. Unexpected data input", None]