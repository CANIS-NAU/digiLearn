import requests
from REST.JSONBuilders import DigiJsonBuilder

URL = "https://www.googleapis.com/customsearch/v1?"
ENGINE_ID = "276d40ae1923ea29f"
API_KEY = "AIzaSyDQ0aKnA5FC2JvcQCtIsl1XwjUsUNAik58"
PARAMS = {}


def make_request(query):
    resultsjson = {}
    url = URL + "key=" + API_KEY + "&cx=" + ENGINE_ID + "&q=" + query

    r = requests.get(url, PARAMS)
    res = r.json()
    results = res["items"] if "items" in res else None

    if results is not None:
        for item in results:
            title = item["title"] if "title" in item else "No Title"
            link = item["link"] if "link" in item else "No Link Found"
            dlink = item["displayLink"] if "displayLink" in item else "No Display Link"
            snip = item["snippet"] if "snippet" in item else "No Snippet"
            mime = item["mime"] if "mime" in item else None
            ff = item["fileFormat"] if "fileFormat" in item else "No File Format"
            DigiJsonBuilder.create_search_result(title, link, dlink, snip, mime, ff)



    return resultsjson


def submit_queries(queries):
    resultsArr = []
    return resultsArr
