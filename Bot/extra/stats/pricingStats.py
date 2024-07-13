import requests
from discord import File
from datetime import datetime
import io
import matplotlib.pyplot as plt
from config import ANALYTICS_API_URI

"""
File Info:
File contains functions to fetch and process game price analytics fetched from the backend
"""

def fetchPricingStats(gameId):
    if gameId != "":
        resp = requests.get(f"{ANALYTICS_API_URI+gameId}&type=pricing")

        if resp.ok:
            try:
                stats = resp.json()
                return [True, "Successfully fetched game pricing stats", stats]
            except:
                return [False, "Could not fetch game pricing stats. Response body invalid", None]

        else:
            return [False, "Could not fetch game Pricing stats. Request unsuccessful", None]
    else:
        return [False, "Could not fetch game Pricing stats. Game ID was not provided", None]

def convertDataToImage_Price(data, embed):
    if data and len(data) > 1:
        try: 
            data_stream = io.BytesIO()
            
            viewers = data[0]
            channels = data[1]

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
            plt.legend(['Viewers', 'Channels'])

            plt.plot([datetime.fromtimestamp(x[0]/1000).hour for x in viewers], [x[1] for x in viewers], color="slateblue", label='Viewers')
            plt.plot([datetime.fromtimestamp(x[0]/1000).hour for x in channels], [x[1] for x in channels], color="springgreen", label='Channels')

            plt.title("Pricing Statistics Over Time", color='lightgreen')
            plt.savefig(data_stream, format='png', bbox_inches="tight", dpi = 80)
            plt.close()

            data_stream.seek(0)
            chart = File(data_stream, filename="price_stats.png")

            embed.set_image(
                url="attachment://price_stats.png"
            )
            
            return [embed, chart]
        except Exception as e:
            print("[Fruno Error]: Failed to generate graphs")
            return [None, None]

    else:
        return [False, "Could not convert price stats data to image. Unexpected data input", None]