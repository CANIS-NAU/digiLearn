import requests

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
            a = ""



    return resultsjson


def submit_queries(queries):
    resultsArr = []
    return resultsArr
