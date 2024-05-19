import { Hono } from 'hono'
import { HTTPException } from 'hono/http-exception'

const app = new Hono()

async function validateGame(gameName: string): Promise<[boolean, string, any, any]> {
  const payload = {"query": gameName,"attributesToHighlight":[],"attributesToSnippet":[],"facets":["tags"],"facetFilters":[["appType:Game"]],"hitsPerPage":100,"attributesToRetrieve":["lastUpdated","name","objectID","followers","oslist","releaseYear","tags","technologies","userScore"]}
  let response: any = await fetch("https://94he6yatei-dsn.algolia.net/1/indexes/steamdb/query", {
    method: "POST",
    headers: {
      'x-algolia-api-key': '9ba0e69fb2974316cdaec8f5f257088f',
      'x-algolia-application-id': '94HE6YATEI',
      'Referer': 'https://www.protondb.com/'
    },
    body: JSON.stringify(payload)
  })

  console.log(response);

  if (response.ok) {
    response = await response.json();
    if (response['hits'].length > 0) {
      return [true, 'Game Found', response['hits'][0].name, response];
    }
    else
    {
      return [false, 'Could not find game with current name', null, null];
    }
  }
  else
  {
    return [false, 'Request to validate game did not go as planned', null, null];
  }
}

async function fetchLinuxInfo(gameId: number): Promise<[boolean, string, any, any]> {
  return await [false, "", null, null];
}

function fetchPlayerData(gameId: number) {
  
}

function fetchPricingData(gameIdentifier: number | string) {

}

function fetchDownloadData(gameIdentifier: number | string) {

}

app.get('/', (c) => {
  return c.text('Welcome to the Fruno API. Endpoints are listed below.')
})

app.get('/fetch', async(c) => {
  const gameName = c.req.query('name');
  if (gameName != undefined) {
    const [success, reason, name, gameResult] = await validateGame(gameName);
    if (success) {
      let gameName = name;
      let gameId = gameResult['hits'][0]['objectID']; 
      let userScore = gameResult['hits'][0]['userScore']; 



    }
    else
    {
      return c.text(reason);
    }


  }
  else
  {
    throw new HTTPException(401, { message: "Name query paramter can't be null" });
  }
})

export default app
