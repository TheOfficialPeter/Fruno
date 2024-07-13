import requests
from humanize import intcomma
from discord import File
from datetime import datetime, timezone
import io
import matplotlib.pyplot as plt
from matplotlib import ticker
from config import ANALYTICS_API_URI

"""
File Info:
File contains functions to fetch and process player analytics fetched from the backend
"""

def fetchPlayerStats(gameId):
    if gameId != "":
        resp = requests.get(f"{ANALYTICS_API_URI+gameId}&type=player")

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

def convert_data_to_image_player(data, embed):
    """
    Converts player data to an image and updates the provided embed with the image.

    Parameters:
        data (list): A list of player data.
        embed (discord.Embed): The embed to be updated with the image.

    Returns:
        list: A list containing the updated embed and the chart file.
            - If the data is valid and the conversion is successful, the list will contain the updated embed and the chart file.
            - If an exception occurs during the conversion, the list will contain None and None.
            - If the data is not valid or the length of the data is less than or equal to 5, the list will contain False, an error message, and None.
    """
    if data and len(data) > 5:
        try: 
            data_stream = io.BytesIO()

            hours = list(map(lambda x: datetime.fromtimestamp(x[0]/1000, tz=timezone.utc).strftime("%H"), data))
            players = list(map(lambda x: x[1], data))

            fig, ax = plt.subplots(figsize=(15,5))

            class HumanizeFormatter(ticker.Formatter):
                def __call__(self, y, pos=None):
                    return intcomma(int(y))

            ax.yaxis.set_major_formatter(HumanizeFormatter())
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
            plt.ylabel("Players", color='lightgreen')
            plt.plot(hours, players, color='lightgreen')
            plt.title("Player Statistics Over Time", color='lightgreen')
            plt.savefig(data_stream, format='png', bbox_inches="tight", dpi=80)
            plt.close()

            data_stream.seek(0)
            chart = File(data_stream, filename="player_stats.png")

            embed.set_image(url="attachment://player_stats.png")
            
            return [embed, chart]
        except Exception as e:
            return [None, None]

    else:
        return [False, "Could not convert player stats data to image. Unexpected data input", None]
