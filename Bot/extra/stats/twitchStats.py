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
    """
    Fetches Twitch analytics for a given game ID.

    Args:
        gameId (str): The ID of the game to fetch Twitch analytics for.

    Returns:
        list: A list containing the following elements:
            - bool: True if the game Twitch stats were successfully fetched, False otherwise.
            - str: A success message if the game Twitch stats were successfully fetched, an error message otherwise.
            - dict or None: The fetched Twitch analytics as a dictionary, or None if the game does not contain Twitch analytics.

    Raises:
        None

    Note:
        This function makes a GET request to the backend API to fetch the Twitch analytics for the given game ID.
        The API URI is obtained from the `ANALYTICS_API_URI` constant in the `config` module.
        The request includes the `type=twitch` parameter to specify that Twitch analytics should be fetched.
        If the request is successful, the function attempts to parse the response as JSON and returns the fetched Twitch analytics.
        If the response cannot be parsed as JSON, an error message is returned indicating that the game does not contain Twitch analytics.
        If the request is unsuccessful, an error message is returned indicating that the game Twitch stats could not be fetched.
        If the game ID is not provided, an error message is returned indicating that the game Twitch stats could not be fetched.
    """
    if gameId != "":
        resp = requests.get(f"{ANALYTICS_API_URI+gameId}&type=twitch")

        if resp.ok:
            try:
                stats = resp.json()
                return [True, "Successfully fetched game twitch stats", stats]
            except:
                return [False, "Could not fetch game twitch stats. This game does not contain Twitch analytics", None]
        else:
            return [False, "Could not fetch game Twitch stats. Request unsuccessful", None]
    else:
        return [False, "Could not fetch game Twitch stats. Game ID was not provided", None]

def convert_twitch_data_to_image(twitch_data, embed):
    """
    Converts Twitch data to an image and attaches it to a Discord embed.

    Args:
        twitch_data (list): A list of tuples containing Twitch data. The first tuple contains viewers data,
            and the second tuple contains channels data. Each tuple contains a timestamp and a value.
        embed (discord.Embed): The Discord embed to attach the image to.

    Returns:
        list: A list containing the updated Discord embed and the attached image file. If the conversion is
            successful, the list will contain the embed and the image file. If the conversion fails, the list
            will contain [False, "Could not convert twitch stats data to image. Unexpected data input", None].

    Raises:
        None

    Notes:
        - The function sorts the Twitch data by timestamp and plots the viewers and channels data over time.
        - The resulting image is saved as "twitch_stats.png" and attached to the Discord embed.
        - The function assumes that the input data is in the correct format and that the matplotlib library is
          installed.
    """
    if twitch_data and len(twitch_data) > 1:
        try:
            output_stream = io.BytesIO()

            viewers_hours, viewers_values = zip(*sorted(
                ((datetime.fromtimestamp(viewer[0] / 1000).strftime("%H"), viewer[1])
                for viewer in twitch_data[0])))

            channels_hours, channels_values = zip(*sorted(
                ((datetime.fromtimestamp(channel[0] / 1000).strftime("%H"), channel[1])
                for channel in twitch_data[1])))

            fig, ax = plt.subplots(figsize=(15, 5))

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
            plt.ylabel("Channels | Viewers", color='lightgreen')
            plt.legend(['Viewers', 'Channels'])

            plt.plot(viewers_hours, viewers_values, color="slateblue", label='Viewers')
            plt.plot(channels_hours, channels_values, color="springgreen", label='Channels')

            plt.title("Twitch Viewer Statistics Versus Twitch Channel Statistic Over Time", color='lightgreen')
            plt.savefig(output_stream, format='png', bbox_inches="tight", dpi=80)
            plt.close()

            output_stream.seek(0)
            chart = File(output_stream, filename="twitch_stats.png")

            embed.set_image(
                url="attachment://twitch_stats.png"
            )

            return [embed, chart]
        except Exception as e:
            print(e)
            return [None, None]

    else:
        return [False, "Could not convert twitch stats data to image. Unexpected data input", None]
