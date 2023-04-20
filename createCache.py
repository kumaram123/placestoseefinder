import requests
from bs4 import BeautifulSoup
import json

CACHE_DICT = {}
API_CACHE_DICT = {}

# Define the Parameters of the search
PARAMETERS = {}

# Define API Key, Search Type, and header
MY_API_KEY = 'F2RKhJmPDzE1S96XmXJVqWAgIkO5HIkdMk_oiM2CC9OeiZ160WjEjA_-bvGelffn045jMJGw90l7zdeQgCkdPnsa39bs4RidFWlt0kb30rR_NOAocISscC-KfAEKZHYx'
HEADERS = {'Authorization': 'bearer %s' % MY_API_KEY}


def set_location(user_search_location):
    PARAMETERS['location'] = user_search_location

def construct_unique_key(baseurl, api_baseurl, params):
    """# for API data
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    api_unique_key = api_baseurl + connector + connector.join(param_strings)"""

    # for web scraping
    unique_key = baseurl
    api_unique_key = api_baseurl

    return unique_key, api_unique_key

def open_cache(CACHE_FILENAME, API_CACHE_FILENAME):
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()

        api_cache_file = open(API_CACHE_FILENAME, 'r')
        api_cache_contents = api_cache_file.read()
        api_cache_dict = json.loads(api_cache_contents)
        api_cache_file.close()
    except:
        cache_dict = {}
        api_cache_dict = {}

    return cache_dict, api_cache_dict

def save_cache(cache_dict, api_cache_dict, CACHE_FILENAME, API_CACHE_FILENAME):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict, indent=3)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

    api_dumped_json_cache = json.dumps(api_cache_dict, indent=3)
    fw = open(API_CACHE_FILENAME,"w")
    fw.write(api_dumped_json_cache)
    fw.close()

def make_request(baseurl, api_baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    response = requests.get(baseurl, headers=HEADERS, params=params)
    api_response = requests.get(api_baseurl, headers=HEADERS, params=params)
    return response.json(), api_response.json()

def make_request_with_cache(baseurl, api_baseurl, params, CACHE_FILENAME, API_CACHE_FILENAME):
    '''Check the cache for a saved result for this baseurl+params
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    request_key, api_request_key = construct_unique_key(baseurl, api_baseurl, params)
    if request_key in CACHE_DICT.keys() and api_request_key in API_CACHE_DICT.keys():
        print("Web Scrape cache hit!", request_key)
        print("API cache hit!", api_request_key)
        return CACHE_DICT[request_key], API_CACHE_DICT[api_request_key]
    else:
        print("Web scrape cache miss!", request_key)
        print("API cache miss!", api_request_key)
        CACHE_DICT[request_key], API_CACHE_DICT[api_request_key] = make_request(baseurl, api_baseurl, params)

        save_cache(CACHE_DICT, API_CACHE_DICT, CACHE_FILENAME, API_CACHE_FILENAME)

        return CACHE_DICT[request_key], API_CACHE_DICT[api_request_key]

def yelp_scrape_or_API(user_search_location):
    # for web scraping data
    if ' ' in user_search_location:
        location = user_search_location.strip().replace(' ', "%20")
        BUSINESS_PATH = 'https://www.yelp.com/search/snippet?find_desc=attractions&find_loc=' + location + '&sortby=rating&request_origin=user'
    else:
        BUSINESS_PATH = 'https://www.yelp.com/search/snippet?find_desc=attractions&find_loc=' + user_search_location + '&sortby=rating&request_origin=user'
    CACHE_FILENAME = "yelp_scraping_cache" + "_" + user_search_location + ".json"

    # for API data
    API_BUSINESS_PATH = 'https://api.yelp.com/v3/categories'
    API_CACHE_FILENAME = "yelp_API_cache" + "_" + user_search_location + ".json"

    return BUSINESS_PATH, CACHE_FILENAME, API_BUSINESS_PATH, API_CACHE_FILENAME