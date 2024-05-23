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

async function fetchLinuxInfo(gameId: number): Promise<[boolean, string, any]> {
  let response = await fetch(`https://www.protondb.com/api/v1/reports/summaries/${gameId.toString()}.json`);
  
  if (response.ok) {
    let linuxGameData = await response.json();
    return [true, "Successfully fetched linux game data", linuxGameData];
  }
  return [false, "", null];
}

async function fetchMediaData(gameId: number): Promise<[boolean, string, any]> {
  const headers = new Headers()
  headers.set('Set-Cookie', "browserid=3557358018393846067")
  headers.set('Set-Cookie', "steamCountry=BR|81a96a64893a3c88b2def9d41bd1c085")

  let response = await fetch(`https://www.protondb.com/proxy/steam/api/appdetails/?appids=${gameId.toString}`, {headers: headers});
  console.log(await response.text());

  if (response.ok) {
    let mediaData = await response.json();
    return [true, "Successfully fetched game media data", mediaData];
  }
  return [false, "", null];
}

async function fetchPlayerData(gameId: number): Promise<[boolean, string, any]> {
  let response = await fetch(`https://steamcharts.com/app/${gameId.toString()}/chart-data.json`)
  
  if (response.ok) {
    let playerData = await response.json();
    return [true, "Successfully fetch game player data", playerData];
  }
  return [true, "", null];
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
  let gameInfoResult: any = {};

  if (gameName != undefined) {
    var [validateSuccess, validateReason, validateName, validateGameResult] = await validateGame(gameName);
    if (validateSuccess) {
      var name = validateName;
      var gameId = validateGameResult['hits'][0]['objectID']; 
      var userScore = validateGameResult['hits'][0]['userScore']; 
    }
    else
    {
      return c.text(validateReason);
    }

    gameInfoResult['name'] = name;
    gameInfoResult['gameId'] = gameId;
    gameInfoResult['userScore'] = userScore;
    
    let [linuxSuccess, linuxReason, linuxGameResult] = await fetchLinuxInfo(gameId);

    if (linuxSuccess) {
      let tier = linuxGameResult['tier'];
      gameInfoResult['tier'] = tier;
    }
    else
    {
      return c.text(linuxReason);
    }

    var [mediaSuccess, mediaReason, mediaResult] = await fetchMediaData(gameId);

    if (mediaSuccess) {
      let headerImage = mediaResult[gameId]['data']['header_image'];
      let trailer = mediaResult[gameId]['data']['movies'][0]['webm']['480'];
      gameInfoResult['image'] = headerImage;
      gameInfoResult['trailer'] = trailer;
    }
    else 
    {
      return c.text(mediaReason);
    }

    let [playerSuccess, playerReason, playerDataResult] = await fetchPlayerData(gameId);

    if (playerSuccess) {
      let currentlyPlaying = playerDataResult.at(-1)[1];
      gameInfoResult['currentPlaying'] = currentlyPlaying;
    }
    else
    {
      return c.text(playerReason);
    }

    return c.json(gameInfoResult);
  }
  else
  {
    throw new HTTPException(401, { message: "Name query paramter can't be null" });
  }
})

export default app
