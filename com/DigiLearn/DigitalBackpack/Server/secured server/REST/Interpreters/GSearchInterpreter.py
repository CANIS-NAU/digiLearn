import requests
from REST.JSONBuilders import DigiJsonBuilder

URL = "https://www.googleapis.com/customsearch/v1?"
ENGINE_ID = "276d40ae1923ea29f"
API_KEY = "API KEY FOR DIGIPACK API"
PARAMS = {}


def make_request(query, modifiers):

    resultsarr = []
    query = append_modifiers(query, modifiers)
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


def submit_queries(queries, modifiers):
    resultsArr = []

    for query in queries:
        r = make_request(query, modifiers)
        results = DigiJsonBuilder.create_results(query, False, len(r), r)
        resultsArr.append(results)
    return resultsArr


def append_modifiers(query, modifiers):
    minsite = " -site:"
    bs = modifiers["blacksite"]
    bt = modifiers["blackterms"]

    bsstr = ""
    for site in bs:
        bsstr = bsstr + minsite + site
    print(bsstr)

    btstr = ""
    for term in bt:
        btstr = btstr + ' -"' + term + '"'
    print(btstr)

    newquery = query + bsstr + btstr

    return newquery