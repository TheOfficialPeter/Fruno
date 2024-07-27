def process_game_info(apiResponse):
    if apiResponse.ok:
        try:
            apiResponse = apiResponse.json()

            match apiResponse['tier'].lower():
                case "bronze":
                    apiResponse['desc'] = ' (Game has significant compatibility issues on Linux with Proton)'
                case "silver":
                    apiResponse['desc'] = ' (Game has minor compatibility problems on Linux with Proton)'
                case "gold":
                    apiResponse['desc'] = ' (Game runs very well on Linux with Proton)'
                case "platinum":
                    apiResponse['desc'] = ' (Game runs flawlessly on Linux with Proton)'
                case "borked":
                    apiResponse['desc'] = ' (Game is completely broken and unplayable on Linux with Proton)'
                case _:
                    apiResponse['desc'] = ' (Invalid ProtonDB tier. Linux game compatibility is unknown)'

            return [True, "Game information fetched successfully", apiResponse]
        except Exception as e:
            print("[ERROR] Failed to parse JSON response for Fetch Command: ", str(e))
            return [False, "Could not fetch game information. response body invalid", None]
    else:
        return [False, "Could not fetch game information. Request unsuccessful", None]