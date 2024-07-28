import requests
from config import SIMILAR_GAMES_API_URI
from Logic.Process.processSimilarGames import process_similar_games

def fetch_similar_games(gameId):
    if gameId != "":
        apiResponse = requests.get(f"{SIMILAR_GAMES_API_URI+gameId}")
        success, message, apiResponse = process_similar_games(apiResponse)

        if not success:
            return [False, message, None]

        return [True, "Successfully fetched similar games", apiResponse]
    else:
        return [False, "Could not fetch similar games. Game ID not provided", None]

