def process_similar_games(apiResponse):
    if apiResponse.ok:
        try:
            similarGames = apiResponse.json()
            return [True, "Successfully processed similar games", similarGames]
        except Exception as e:
            print("[ERROR] Failed to parse JSON response for Fetch Command: ", str(e))
            return [False, "Could not fetch similar games. response body invalid", None]
    else:
        print("[ERROR] Failed to fetch similar games. Request unsuccessful. Status Code: ", apiResponse.status_code)
        return [False, "Could not fetch similar games. Request unsuccessful", None]