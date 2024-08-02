def process_game_info(apiResponse):
    if apiResponse.ok:
        try:
            apiResponse = apiResponse.json()

            return [True, "Game information fetched successfully", apiResponse]
        except Exception as e:
            print("[ERROR] Failed to parse JSON response for Fetch Command: ", str(e))
            return [False, "Could not fetch game information. response body invalid", None]
    else:
        return [False, "Could not fetch game information. Request unsuccessful", None]