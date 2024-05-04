import { Hono } from 'hono'
import { HTTPException } from 'hono/http-exception'

const app = new Hono()

async function validate(gameName: string):[boolean, string, any, any] {
  if ( gameName != null && gameName != "" && gameName != " " ) {
    var protonResponse = await fetch("https://94he6yatei-dsn.algolia.net/1/indexes/steamdb/query", {
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
      return [false, 'Request to ProtonDB failed. Status did not return OK'];
    }

    protonResponse = await protonResponse.json();

    if ( 'hits' in protonResponse && protonResponse['hits'].length > 0) {
      var protonTierResponse = await fetch(`https://www.protondb.com/api/v1/reports/summaries/${ protonResponse['hits'][0]['objectID'] }.json`)
      protonTierResponse = await protonTierResponse.json();

      return [true, 'Request to ProtonDB succeeded', protonResponse, protonTierResponse];
    }
    else if ( 'hits' in protonResponse )
    {
      return [false, 'Game not found']
    }
    else
    {
      return [false, 'It seems that ProtonDB might have changed their API. Please wait for an update'];
    }
  }
  else
  {
    return [false, 'Game name was not provided. Please try again'];
  }
}

function extractValues(protonResponse, protonTier): [boolean, string, any] {
  if ( protonResponse != null && Object.keys(protonResponse).length > 0 && protonTier != null && Object.keys(protonTier).length > 0 ) {
    const firstGame = protonResponse['hits'][0];

    return [true, "Values extracted successfully", {name: firstGame['name'], userScore: firstGame['userScore'], tier: protonTier['tier']} ];
  }
  else
  {
    return [false, 'Please provide a valid ProtonDB game info object AND ProtonDB game tier object'];
  }
}

app.get('/', (c) => {
  throw new HTTPException(404, {message: 'Route Not Found. Did you perhaps mean /fetch?'})
})

app.get('/fetch', async (c, next) => {
  var [success, reason, results, tier] = await validate(c.req.query('name'));

  if ( success ) {
    [success, reason, results] = extractValues(results, tier);

    if ( success ) {
      return c.json(results);
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
