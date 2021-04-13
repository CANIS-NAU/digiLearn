import requests
from REST.JSONBuilders import DigiJsonBuilder

URL = "https://www.googleapis.com/customsearch/v1?"
ENGINE_ID = "276d40ae1923ea29f"
API_KEY = "AIzaSyCOAsr-SldNjop-SAQxb9HoY1E0KrIYDaE"
PARAMS = {}


def make_request(query):
    resultsarr = []
    # build query url
    u = URL + "key=" + API_KEY + "&cx=" + ENGINE_ID + "&q=" + query
    # make request
    r = requests.get(u, PARAMS)
    # pull json from request
    res = r.json()
    # pull "items" from results
    results = res["items"] if "items" in res else None

    if results is not None:
        for item in results:
            title = item["title"] if "title" in item else "No Title"
            link = item["link"] if "link" in item else "No Link Found"
            dlink = item["displayLink"] if "displayLink" in item else "No Display Link"
            snip = item["snippet"] if "snippet" in item else "No Snippet"
            mime = item["mime"] if "mime" in item else None
            ff = item["fileFormat"] if "fileFormat" in item else "No File Format"
            rjson = DigiJsonBuilder.create_search_result(title, link, dlink, snip, mime, ff)
            resultsarr.append(rjson)

    return resultsarr


def submit_queries(queries):
    resultsArr = []

    for query in queries:
        r = make_request(query)
        results = DigiJsonBuilder.create_results(query, False, len(r), r)
        resultsArr.append(results)
    return resultsArr
