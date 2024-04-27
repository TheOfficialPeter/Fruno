import requests
import json
import cloudscraper
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

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

def steamdb(number: str = ""):
    print(f"Handling request to /steamdb with number: {number}")
    if number:
        url = f"https://steamdb.info/app/{number}"
        try:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url)

            if response.status_code == 200:
                print("Received successful response from SteamDB")
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the ul element with the class 'app-chart-numbers-big'
                app_chart_numbers = soup.find('ul', {'class': 'app-chart-numbers-big'})

                # Extract the text values from the li elements
                text_values = [li.get_text(strip=True) for li in app_chart_numbers.find_all('li')]

                return {"status": "Success", "data": text_values, "status_text": response.text}
            else:
                print(f"Failed to fetch data from SteamDB for number: {number}")
                return {"status": "Error", "message": f"Failed to fetch data from SteamDB for number: {number}, status code: {response.status_code}", "status_text": response.text}
        except Exception as e:
            print(f"Error fetching data from SteamDB for number: {number}")
            return {"status": "Error", "message": f"Error fetching data from SteamDB for number: {number}, error: {str(e)}", "status_text": ""}
    else:
        print("No number provided, returning a message")
        return "Please provide a number for the SteamDB request"

@app.get("/")
async def index():
    print("Handling request to root URL (/)")
    return {"message": "Hello World"}

@app.get("/fetch")
async def fetch(name: str = ""):
    print(f"Handling request to /fetch with name: {name}")
    global payload

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
