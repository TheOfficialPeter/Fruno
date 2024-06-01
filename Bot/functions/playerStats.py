import requests

def fetchPlayerStats(gameId):
    if gameId != "":
        resp = requests.get(f"https://6651005cb09f1b83aa75.appwrite.global/?gameid={gameId}")

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

def convertDataToImage(data):
    if data and len(data) > 5:
        pass
        # Create image from data
        for hour in reversed(range(len(data), 0)):
            print(hour)
    else:
        return [False, "Could not convert player stats data to image. Unexpected data input", None]