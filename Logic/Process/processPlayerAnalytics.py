def process_player_analytics(apiResponse):
    if apiResponse.ok:
        try:
            gameAnalytics = apiResponse.json()
            return [True, "Successfully processed game player stats", gameAnalytics]
        except Exception as e:
            print("[ERROR] Failed to parse JSON response for Fetch Command: ", str(e))
            return [False, "Could not fetch game player stats. response body invalid", None]
    else:
        print("[ERROR] Failed to fetch game player stats. Request unsuccessful. Status Code: ", apiResponse.status_code)
        return [False, "Could not fetch game player stats. Request unsuccessful", None]