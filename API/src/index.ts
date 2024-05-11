import { Hono } from 'hono'
import { HTTPException } from 'hono/http-exception'
import { cors } from 'hono/cors'

const app = new Hono()
app.use('*', cors())

async function validate(gameName: string): Promise<[boolean, string, any, any]> {
  if (!gameName || gameName.trim() === "") {
    return [false, 'Game name was not provided. Please try again', null, null];
  }

  try {
    const protonResponse: any = await fetch("https://94he6yatei-dsn.algolia.net/1/indexes/steamdb/query", {
      method: "POST",
      body: JSON.stringify({
        "query": gameName,
        "attributesToHighlight": [],
        "attributesToSnippet": [],
        "facets": ["tags"],
        "facetFilters": [["appType:Game"]],
        "hitsPerPage": 50,
        "attributesToRetrieve": ["lastUpdated", "name", "objectID", "followers", "oslist", "releaseYear", "tags", "technologies", "userScore"],
        "page": 0
      }),
      headers: {
        "Content-Type": "application/json",
        "x-algolia-api-key": "9ba0e69fb2974316cdaec8f5f257088f",
        "x-algolia-application-id": "94HE6YATEI",
        "Referer": "https://www.protondb.com/"
      }
    });

    if (!protonResponse.ok) {
      return [false, 'Request to ProtonDB failed. Status did not return OK', null, null];
    }

    const protonResponseData = await protonResponse.json();

    if ('hits' in protonResponseData && protonResponseData['hits'].length > 0) {
      const protonTierResponse = await fetch(`https://www.protondb.com/api/v1/reports/summaries/${protonResponseData['hits'][0]['objectID']}.json`);
      const protonTierResponseData = await protonTierResponse.json();
      return [true, 'Request to ProtonDB succeeded', protonResponseData, protonTierResponseData];
    } else if ('hits' in protonResponseData) {
      return [false, 'Game not found', null, null];
    } else {
      return [false, 'It seems that ProtonDB might have changed their API. Please wait for an update', null, null];
    }
  } catch (err) {
    return [false, 'Request to ProtonDB failed. Could not convert to JSON', null, null];
  }
}

function extractValues(protonResponse: any, protonTier: any): [boolean, string, any] {
  if ( protonResponse != null && Object.keys(protonResponse).length > 0 && protonTier != null && Object.keys(protonTier).length > 0 ) {
    const firstGame = protonResponse['hits'][0];

    return [true, "Values extracted successfully", {name: firstGame['name'], userScore: firstGame['userScore'], tier: protonTier['tier'], gameId: firstGame['objectID']} ];
  }
  else
  {
    return [false, 'Please provide a valid ProtonDB game info object AND ProtonDB game tier object', null];
  }
}

async function getSteamMedia(gameId: number): Promise<[boolean, string, any]> {
  try {
    let response: any = await fetch("https://www.protondb.com/proxy/steam/api/appdetails/?appids=" + gameId.toString(), {
      headers: {
          "referrer": "https://www.protondb.com/app/" + gameId.toString(),
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
          "Accept": "*/*",
          "Accept-Language": "en-US,en;q=0.5",
          "Sec-Fetch-Dest": "empty",
          "Sec-Fetch-Mode": "cors",
          "Sec-Fetch-Site": "same-origin",
          "mode": "cors",
      },
      method: "GET",
    });

    response = await response.json();

    const gameImage = response[gameId]['data']['header_image'];
    const gameTrailer = response[gameId]['data']['movies'][0]['mp4']['480'];
    return [true, 'Media fetched successfully', {image: gameImage, trailer: gameTrailer}];
  } catch (err) {
    return [false, 'Request to Steam API failed. Could not convert to JSON', null];
  }
}

app.get('/', (c) => {
  throw new HTTPException(404, {message: 'Route Not Found. Did you perhaps mean /fetch?'})
})

app.get('/fetch', async (c, next) => {
  try {
    // -- Validate
    const [success, reason, results, tier] = await validate(c.req.query('name') as string);

    if (!success) {
      return c.text(`Validation Failed. Reason: ${reason}`, 500);
    }

    // -- Extract
    const [extractSuccess, extractReason, extractedValues] = extractValues(results, tier);

    if (!extractSuccess) {
      return c.text(`Something went wrong when extracting values from ProtonDB. Reason: ${extractReason}`, 500);
    }

    // -- Media
    const [mediaSuccess, mediaReason, media] = await getSteamMedia(extractedValues.gameId);

    if (!mediaSuccess) {
      return c.text(`Error occurred while fetching media from Steam. Reason: ${mediaReason}`, 500);
    }

    // -- Return
    extractedValues.media = media;
    return c.json(extractedValues);
  } catch (error: any) {
    return c.text(`Something went wrong. Reason: ${error.message}`, 500);
  }
});

export default app


