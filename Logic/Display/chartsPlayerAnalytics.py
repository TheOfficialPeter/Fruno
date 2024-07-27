from humanize import intcomma
from discord import File
from datetime import datetime, timezone
import io
import matplotlib.pyplot as plt
from matplotlib import ticker

def convert_data_to_image_player(embedData):
    embed, playerData = embedData
    if playerData and len(playerData) > 5:
        try: 
            data_stream = io.BytesIO()

            hours = list(map(lambda x: datetime.fromtimestamp(x[0]/1000, tz=timezone.utc).strftime("%H"), playerData))
            players = list(map(lambda x: x[1], playerData))

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
            
            return [True, "Successfully generated player statistics chart", embed, chart]
        except Exception as e:
            print("[ERROR] Failed to convert player stats data to image: ", str(e))
            return [False, "Failed to convert player stats data to image. Please try again later.", None]

    else:
        return [False, "Could not convert player stats data to image. Unexpected data input", None]