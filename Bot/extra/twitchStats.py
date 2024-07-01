import requests
from discord import File
from datetime import datetime
import io
import matplotlib.pyplot as plt
from config import ANALYTICS_API_URI

"""
File Info:
File contains functions to fetch and process twitch analytics fetched from the backend
"""

def fetchTwitchStats(gameId):
    if gameId != "":
        resp = requests.get(f"{ANALYTICS_API_URI+gameId}&type=twitch")

        if resp.ok:
            try:
                stats = resp.json()
                return [True, "Successfully fetched game twitch stats", stats]
            except:
                return [False, "Could not fetch game twitch stats. Response body invalid", None]

        else:
            return [False, "Could not fetch game twitch stats. Request unsuccessful", None]
    else:
        return [False, "Could not fetch game twitch stats. Game ID not provided", None]

def convertDataToImage_Twitch(data, embed):
    if data and len(data) > 5:
        try: 
            data_stream = io.BytesIO()

            time = list(map(lambda x: datetime.utcfromtimestamp(x[0]/1000).strftime("%H"), data))
            viewers = list(map(lambda x: x[1], data))

            fig, ax = plt.subplots(figsize=(15,5))

            ax.set_facecolor('#23272A')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.grid(color='gray', linestyle='--', linewidth=0.5)
            fig.patch.set_facecolor('#23272A')

            plt.xlabel("Time", color='lightgreen')
            plt.ylabel("Viewers", color='lightgreen')
            plt.plot(time, viewers, color='lightgreen')
            plt.title("Twitch Viewer Statistics Over Time", color='lightgreen')
            plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
            plt.close()

            data_stream.seek(0)
            chart = File(data_stream, filename="twitch_stats.png")

            embed.set_image(
                url="attachment://twitch_stats.png"
            )
            
            return [embed, chart]
        except Exception as e:
            print("[Fruno Error]: Failed to generate graphs")
            return [None, None]

    else:
        return [False, "Could not convert twitch stats data to image. Unexpected data input", None]