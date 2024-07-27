from config import API_URI
from Logic.Process.processGameInfo import process_game_info
import requests

def fetch_game_info(gameName):
    apiResponse = requests.get(API_URI + gameName, timeout=50)
    success, message, apiResponse = process_game_info(apiResponse)           

    return [True, "Game information fetched successfully", apiResponse] if success else [False, message, None]
        