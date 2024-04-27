import requests
import json
import cloudscraper
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()


def steamdb(number: str = ""):
    """
    Fetch data from SteamDB for a given game number.
    """
    print(f"Handling request to /steamdb with number: {number}")
    if number:
        url = f"https://steamdb.info/app/{number}"
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Alt-Used": "steamdb.info",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1"
            }

            cookies = {
                "__cf_bm": "Bm.L70ZBVDPIBYT13DaZFXSI4rk6L8HFvLZX6uIuH4g-1714226892-1.0.1.1-8JGbMAD8hvFt1tLXTvcT_5IZdza3ZhRdgzUMz5VPVcUNTyx.AYq0tcHdoCMadDU4kvbuNoXsj948FaIXEdY2IQ",
                "cf_clearance": "epYYau51_8uYdMRwRg4u_9H_RrohoBhKDpbm4O7cIQI-1714215584-1.0.1.1-sIywkIdwsTEqB2lysg7XjqiDw3idAaXP2aNZprd62WrZbFoqaLYhEyYtoQfpOAWt0.SfVZ0f3ryTwF0oSO6Y.w"
            }

            scraper = cloudscraper.create_scraper()
            response = scraper.get(url, headers=headers, cookies=cookies)

            if response.status_code == 200:
                print("Received successful response from SteamDB")
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the div element with the selector 'div.header-thing-number:nth-child(1)'
                header_thing_number = soup.select_one('div.header-thing-number:nth-child(1)')

                if header_thing_number:
                    text_value = header_thing_number.get_text(strip=True)
                    return {"status": "Success", "data": [text_value]}
                else:
                    print(f"Could not find the 'header-thing-number' element on the page for number: {number}")
                    return {"status": "Error", "message": f"Could not find the 'header-thing-number' element on the page for number: {number}"}
            else:
                print(f"Failed to fetch data from SteamDB for number: {number}")
                return {"status": "Error", "message": f"Failed to fetch data from SteamDB for number: {number}, status code: {response.status_code}"}
        except Exception as e:
            print(f"Error fetching data from SteamDB for number: {number}")
            return {"status": "Error", "message": f"Error fetching data from SteamDB for number: {number}, error: {str(e)}"}
    else:
        print("No number provided, returning a message")
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Please provide a number for the SteamDB request")

@app.get("/")
async def index():
    print("Handling request to root URL (/)")
    return {"message": "Hello World"}

@app.get("/fetch")
async def fetch(name: str = ""):
    print(f"Handling request to /fetch with name: {name}")

    if name:
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
            print(f"Extracted objectID: {objectID}")

            print("Sending GET request to ProtonDB API")
            url = f"https://www.protondb.com/api/v1/reports/summaries/{objectID}.json"
            protondb_response = requests.get(url)

            if protondb_response.status_code == 200:
                print("Received successful response from ProtonDB API")
                protondb_data = protondb_response.json()
                extracted_data = {
                    "confidence": protondb_data.get("confidence"),
                    "score": protondb_data.get("score"),
                    "total": protondb_data.get("total"),
                    "tier": protondb_data.get("tier"),
                    "name": firstResult.get("name"),
                    "userScore": firstResult.get("userScore")
                }
                print("Extracted relevant data from ProtonDB response")

                # Call the steamdb function to fetch data from SteamDB
                steamdb_data = steamdb(objectID)

                return {"objectID": objectID, "protondb_data": extracted_data, "steamdb_data": steamdb_data}
            else:
                print(f"Failed to fetch data from ProtonDB for ObjectID: {objectID}")
                return f"Failed to fetch data from ProtonDB for ObjectID: {objectID}"
        else:
            print(f"Could not find any results for: {name}")
            return f"Could not find any results for: {name}"
    else:
        print("No name provided, returning a message")
        return "Please provide a name of a game to validate"
