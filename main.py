import requests
import json
import cloudscraper
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
    print("Handling request to root URL (/)")
    return {"message": "Hello World"}

@app.get("/fetch")
async def fetch(name: str = ""):
    print(f"Handling request to /fetch with name: {name}")
    payload = {
        "query": "",
        "attributesToHighlight": [],
        "attributesToSnippet": [],
        "facets": ["tags"],
        "facetFilters": [["appType:Game"]],
        "hitsPerPage": 50,
        "attributesToRetrieve": ["lastUpdated", "name", "objectID", "followers", "oslist", "releaseYear", "tags", "technologies", "userScore"],
        "page": 0
    }

    if name:
        print("Updating payload with the provided name")
        payload["query"] = name
        payload = json.dumps(payload)

        print("Sending POST request to Algolia API")
        response = requests.post("https://94he6yatei-dsn.algolia.net/1/indexes/steamdb/query?x-algolia-agent=Algolia for JavaScript (4.23.3); Browser", headers={"x-algolia-api-key": '9ba0e69fb2974316cdaec8f5f257088f', 'x-algolia-application-id': '94HE6YATEI', 'Referer': 'https://www.protondb.com'}, data=payload)
        response = response.json()

        if len(response['hits']) > 0:
            print("Received response from Algolia API with at least one hit")
            firstResult = response['hits'][0]

            objectID = firstResult['objectID']
            game_name = firstResult['name']
            print(f"Extracted objectID: {objectID}")
            print(f"Extracted Game Name: {game_name}")

            print("Sending GET request to ProtonDB API")
            url = f"https://www.protondb.com/api/v1/reports/summaries/{objectID}.json"
            protondb_response = requests.get(url)

            if protondb_response.status_code == 200:
                image_url = "https://www.protondb.com/proxy/steam/api/appdetails/?appids=" + objectID
                image_response = requests.get(image_url)

                print("Received successful response from ProtonDB API")
                protondb_data = protondb_response.json()
                data = {
                    "confidence": protondb_data.get("confidence"),
                    "score": protondb_data.get("score"),
                    "total": protondb_data.get("total"),
                    "tier": protondb_data.get("tier"),
                    "name": game_name,
                    "userScore": firstResult.get("userScore"),
                    "objectId": objectID,
                    "image": image_response.json()[objectID]["data"]["header_image"]
                }

                return {"data": data}
            else:
                print(f"Failed to fetch data from ProtonDB for ObjectID: {objectID}")
                return f"Failed to fetch data from ProtonDB for ObjectID: {objectID}"
        else:
            print(f"Could not find any results for: {name}")
            return f"Could not find any results for: {name}"
    else:
        print("No name provided, returning a message")
        return "Please provide a name of a game to validate"
