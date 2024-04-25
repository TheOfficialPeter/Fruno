package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"

    "github.com/go-chi/chi"
)

type AlgoliaRequest struct {
    Query                  string   `json:"query"`
    AttributesToHighlight  []string `json:"attributesToHighlight"`
    AttributesToSnippet    []string `json:"attributesToSnippet"`
    Facets                 []string `json:"facets"`
    FacetFilters           [][]string `json:"facetFilters"`
    HitsPerPage            int      `json:"hitsPerPage"`
    AttributesToRetrieve   []string `json:"attributesToRetrieve"`
    Page                   int      `json:"page"`
}

type AlgoliaHit struct {
    ObjectID string `json:"objectID"`
    Name     string `json:"name"`
}

type AlgoliaResponse struct {
    NbHits int           `json:"nbHits"`
    Hits   []AlgoliaHit `json:"hits"`
}

type ProtonDBData struct {
    Tier string `json:"tier"`
}

type ScrapeResponse struct {
    AlgoliaHit
    ProtonDBData
}

type ErrorResponse struct {
    Error string `json:"error"`
}

func main() {
    fmt.Println("Starting web server...")
    r := chi.NewRouter()

    r.Get("/", func(w http.ResponseWriter, r *http.Request) {
        http.ServeFile(w, r, "index.html")
    })

    r.Get("/scrape", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("Received /scrape request")
        name := r.URL.Query().Get("name")
        if name == "" {
            http.Error(w, "Missing 'name' query parameter", http.StatusBadRequest)
            return
        }

        result, err := scrapeAlgolia(name)
        if err != nil {
            fmt.Println("Error scraping data:", "Pending Linux Verification for game")
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(ErrorResponse{Error: "Pending Linux Verification for game"})
            return
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(result)
    })

    fmt.Println("Listening on :8080")
    http.ListenAndServe(":8080", r)
}

func scrapeAlgolia(query string) (ScrapeResponse, error) {
    fmt.Println("Scraping Algolia data for query:", query)
    algoliaRequest := AlgoliaRequest{
        Query:                  query,
        AttributesToHighlight:  []string{},
        AttributesToSnippet:    []string{},
        Facets:                 []string{"tags"},
        FacetFilters:           [][]string{{"appType:Game"}},
        HitsPerPage:            1, // Only grab the first object
        AttributesToRetrieve:   []string{"objectID", "name"},
        Page:                   0,
    }

    url := "https://94he6yatei-dsn.algolia.net/1/indexes/steamdb/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.23.3)%3B%20Browser"

    jsonData, err := json.Marshal(algoliaRequest)
    if err != nil {
        return ScrapeResponse{}, err
    }

    req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    if err != nil {
        return ScrapeResponse{}, err
    }
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("x-algolia-api-key", "9ba0e69fb2974316cdaec8f5f257088f")
    req.Header.Set("x-algolia-application-id", "94HE6YATEI")
    req.Header.Set("Referer", "https://www.protondb.com/")

    client := &http.Client{}
    fmt.Println("Making Algolia API request...")
    resp, err := client.Do(req)
    if err != nil {
        return ScrapeResponse{}, err
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return ScrapeResponse{}, err
    }

    var algoliaResp AlgoliaResponse
    err = json.Unmarshal(body, &algoliaResp)
    if err != nil {
        return ScrapeResponse{}, err
    }

    fmt.Printf("Algolia response received, %d hits found\n", algoliaResp.NbHits)

    if len(algoliaResp.Hits) > 0 {
        hit := algoliaResp.Hits[0]
        fmt.Printf("Fetching ProtonDB data for objectID: %s\n", hit.ObjectID)
        protonDBData, err := fetchProtonDBData(hit.ObjectID)
        if err != nil {
            return ScrapeResponse{}, err
        }

        return ScrapeResponse{
            AlgoliaHit:    hit,
            ProtonDBData:  protonDBData,
        }, nil
    }

    return ScrapeResponse{}, fmt.Errorf("No hits found in the Algolia response")
}

func fetchProtonDBData(objectID string) (ProtonDBData, error) {
    url := fmt.Sprintf("https://www.protondb.com/api/v1/reports/summaries/%s.json", objectID)
    fmt.Printf("Fetching ProtonDB data from: %s\n", url)
    resp, err := http.Get(url)
    if err != nil {
        return ProtonDBData{}, err
    }
    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        return ProtonDBData{}, err
    }

    var protonDBData ProtonDBData
    err = json.Unmarshal(body, &protonDBData)
    if err != nil {
        return ProtonDBData{}, err
    }

    return protonDBData, nil
}

