import requests
from config import ANALYTICS_API_URI
from Logic.Process.processPlayerAnalytics import process_player_analytics

def fetch_player_stats(gameId):
    if gameId != "":
        apiResponse = requests.get(f"{ANALYTICS_API_URI+gameId}&type=player")
        success, message, apiResponse = process_player_analytics(apiResponse)

        if not success:
            return [False, message, None]

        return [True, "Successfully fetched game player stats", apiResponse]
    else:
        return [False, "Could not fetch game player stats. Game ID not provided", None]
