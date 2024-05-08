import { Hono } from 'hono'
import { HTTPException } from 'hono/http-exception'

const app = new Hono()

async function validate(gameName: string): Promise<[boolean, string, any, any]> {
  if ( gameName != null && gameName != "" && gameName != " " ) {
    var protonResponse: any = await fetch("https://94he6yatei-dsn.algolia.net/1/indexes/steamdb/query", {
      method: "POST",
      body: JSON.stringify({"query":gameName,"attributesToHighlight":[],"attributesToSnippet":[],"facets":["tags"],"facetFilters":[["appType:Game"]],"hitsPerPage":50,"attributesToRetrieve":["lastUpdated","name","objectID","followers","oslist","releaseYear","tags","technologies","userScore"],"page":0}),
      headers: { 
        "Content-Type": "application/json",
        "x-algolia-api-key": "9ba0e69fb2974316cdaec8f5f257088f",
        "x-algolia-application-id": "94HE6YATEI",
        "Referer": "https://www.protondb.com/"
      }
    });

    if ( !protonResponse.ok ) {
      return [false, 'Request to ProtonDB failed. Status did not return OK', null, null];
    }

    protonResponse = await protonResponse.json();

    if ( 'hits' in protonResponse && protonResponse['hits'].length > 0) {
      var protonTierResponse: any = await fetch(`https://www.protondb.com/api/v1/reports/summaries/${ protonResponse['hits'][0]['objectID'] }.json`)
      protonTierResponse = await protonTierResponse.json();

      return [true, 'Request to ProtonDB succeeded', protonResponse, protonTierResponse];
    }
    else if ( 'hits' in protonResponse )
    {
      return [false, 'Game not found', null, null];
    }
    else
    {
      return [false, 'It seems that ProtonDB might have changed their API. Please wait for an update', null, null];
    }
  }
  else
  {
    return [false, 'Game name was not provided. Please try again', null, null];
  }
}

async function steamAnalyics(previousResults: any): Promise<[boolean, string, any]> {
  if ( previousResults['gameId'] != null && previousResults['gameId'] > 0 ) {
    let steamResponse: any = await fetch(`https://store.steampowered.com/api/appdetails?appids=${previousResults['gameId']}`);
    steamResponse = await steamResponse.json();
    steamResponse = steamResponse[previousResults['gameId'].toString()]['data'];

    if ( steamResponse['price_overview'] != null && steamResponse['price_overview']['final'] != null ) {
      previousResults['price'] = steamResponse['price_overview']['final'];
    }
    else
    {
      previousResults['price'] = null;
    }
    
    if ( steamResponse['movies'][0] != null && steamResponse['movies'][0]['mp4'] != null && steamResponse['movies'][0]['mp4']['480'] != null ) {
      previousResults['trailer'] = steamResponse['movies'][0]['mp4']['480'];
    }
    else if ( steamResponse['movies'][0] != null && steamResponse['movies'][0]['mp4'] != null && steamResponse['movies'][0]['mp4']['max'] != null )
    {
      previousResults['trailer'] = steamResponse['movies'][0]['mp4']['max'];
    }
    else if ( steamResponse['movies'][0] != null && steamResponse['movies'][0]['webm'] != null && steamResponse['movies'][0]['webm']['480'] != null )
    {
      previousResults['trailer'] = steamResponse['movies'][0]['webm']['480'];
    }
    else if ( steamResponse['movies'][0] != null && steamResponse['movies'][0]['webm'] != null && steamResponse['movies'][0]['webm']['max'] != null )
    {
      previousResults['trailer'] = steamResponse['movies'][0]['webm']['max'];
    }
    else
    {
      previousResults['trailer'] = null;
    }

    return [true, "Steam Analyitcs request succeeded", previousResults]; 
  }
  else
  {
    return [false, "Please provide a valid game ID", null];
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

app.get('/', (c) => {
  throw new HTTPException(404, {message: 'Route Not Found. Did you perhaps mean /fetch?'})
})

app.get('/fetch', async (c, next) => {
  var [success, reason, results, tier] = await validate(c.req.query('name') as string);

  if ( success ) {
    [success, reason, results] = extractValues(results, tier);

    if ( success ) {
      [success, reason, results] = await steamAnalyics(results);

      if ( success ) {
        return c.json(results);
      }
      else
      {
        return c.text(`Something went wrong when extracting values from Steam's API. Reason: ${reason}`, 500);
      }
    }
    else
    {
      return c.text(`Something went wrong when extracting values from ProtonDB. Reason: ${reason}`, 500);
    }
  }
  else
  {
    return c.text(`Something went wrong. Reason: ${reason}`, 500);
  }
})

export default app
