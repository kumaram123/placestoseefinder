import requests
from bs4 import BeautifulSoup
import json
import os
import createCache
from proj_secrets import MY_API_KEY

CACHE_DICT = {}
API_CACHE_DICT = {}

PARAMETERS = {}

# Define API Key, Search Type, and header
#MY_API_KEY = 'F2RKhJmPDzE1S96XmXJVqWAgIkO5HIkdMk_oiM2CC9OeiZ160WjEjA_-bvGelffn045jMJGw90l7zdeQgCkdPnsa39bs4RidFWlt0kb30rR_NOAocISscC-KfAEKZHYx'
HEADERS = {'Authorization': 'bearer %s' % MY_API_KEY}

def set_location(user_search_location):
    PARAMETERS['location'] = user_search_location

def construct_unique_key(baseurl, params, isScrape: bool):
    """if isScrape == False:
        param_strings = []
        connector = '_'
        for k in params.keys():
            param_strings.append(f'{k}_{params[k]}')
        param_strings.sort()
        unique_key = baseurl + connector + connector.join(param_strings)
    else:
        unique_key = baseurl"""
    unique_key = baseurl
    return unique_key

def open_cache(CACHE_FILENAME):
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
    except:
        cache_dict = {}

    return cache_dict

def save_cache(cache_dict, CACHE_FILENAME):
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

def make_request(baseurl, params):
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
    return response.json()

def make_request_with_cache(baseurl, params, CACHE_FILENAME, isScrape: bool):
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
    request_key = construct_unique_key(baseurl, params, isScrape)
    #if request_key in CACHE_DICT.keys():
    #    print("cache hit!", request_key)
    #    return CACHE_DICT[request_key]
    if isScrape == False:
        print("cache miss!", request_key)
        API_CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(API_CACHE_DICT, CACHE_FILENAME)
        return API_CACHE_DICT[request_key]

    if isScrape == True:
        print("cache miss!", request_key)
        CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(CACHE_DICT, CACHE_FILENAME)
        return CACHE_DICT[request_key]

def yelp_scrape_or_API(user_search_location, isScrape):
    if isScrape == True:
        BUSINESS_PATH = []
        if ' ' in user_search_location:
            location = user_search_location.strip().replace(' ', "%20")
            for pag in range(0, 10):
                #time.sleep(5)
                BUSINESS_PATH.append('https://www.yelp.com/search/snippet?find_desc=attractions&find_loc=' + location + '&sortby=rating&start=' + str(pag*10) + '&request_origin=user')
                #BUSINESS_PATH = 'https://www.yelp.com/search/snippet?find_desc=tourist+attractions&find_loc=' + location + '&request_origin=user'
        else:
            for pag in range(0, 10):
                #time.sleep(5)
                BUSINESS_PATH.append('https://www.yelp.com/search/snippet?find_desc=attractions&find_loc=' + user_search_location + '&sortby=rating&start=' + str(pag*10) + '&request_origin=user')
        CACHE_FILENAME = "yelp_scraping_cache" + "_" + user_search_location + ".json"

    if isScrape == False:
        BUSINESS_PATH = 'https://api.yelp.com/v3/categories'
        CACHE_FILENAME = "yelp_API_cache" + "_" + user_search_location + ".json"
    return BUSINESS_PATH, CACHE_FILENAME

def checkCacheExistence(CACHE_FILENAME):
    existingJsonFiles = []
    for x in os.listdir():
        if x.endswith(".json"):
            existingJsonFiles.append(x)

    if CACHE_FILENAME in existingJsonFiles:
        print("Cache hit!: ", CACHE_FILENAME)
        return open_cache(CACHE_FILENAME)

    else:
        return False

def getCache(user_search_location, user_search_category):
    set_location(user_search_location)
    _, _, API_BUSINESS_PATH, API_CACHE_FILENAME = createCache.yelp_scrape_or_API(user_search_location)
    BUSINESS_PATH, CACHE_FILENAME = yelp_scrape_or_API(user_search_location, True)
    locTitle = ""

    if checkCacheExistence(API_CACHE_FILENAME) == False:
        api_results = make_request_with_cache(API_BUSINESS_PATH, PARAMETERS, API_CACHE_FILENAME, False)
    else:
        api_results = checkCacheExistence(API_CACHE_FILENAME)

    if checkCacheExistence(CACHE_FILENAME) == False:
        all_results = []
        for b in BUSINESS_PATH:
            results = make_request_with_cache(b, PARAMETERS, CACHE_FILENAME, True)
            all_results.append(results)
    else:
        all_results = checkCacheExistence(CACHE_FILENAME)

    try:
        x = list(api_results.keys())[0]
        categoriesList = api_results[x]['categories']
    except:
        categoriesList = api_results['categories']

    aliases = []
    for i in categoriesList:
        if user_search_category in i['alias']:
            aliases.append(i['alias'])

    tmp_data = {}

    if type(all_results) is list:
        for r in all_results:
            if 'searchExceptionProps' in r['searchPageProps'].keys() or aliases == []:
                isValid = False

            else:
                isValid = True
                #print(all_results[r]["pageTitle"].split(" - ")[0])
                #locTitle = all_results[r]["pageTitle"].split(" - ")[0]
                search_results = r['searchPageProps']['mainContentComponentsListProps']
                for place in search_results:
                    if place['searchResultLayoutType'] == "iaResult":
                        for i in range(len(place["searchResultBusiness"]["categories"])):
                            for a in aliases:
                                if a in place["searchResultBusiness"]["categories"][i]["title"].lower():
                                    tmp_data[place['searchResultBusiness']['name']] = {
                                        'name': place['searchResultBusiness']['name'],
                                        'rating': place['searchResultBusiness']['rating'],
                                        'reviewCount': place['searchResultBusiness']['reviewCount'],
                                        'url': "https://www.yelp.com" + place["searchResultBusiness"]["businessUrl"],
                                        'phone_num': place['searchResultBusiness']['phone'],
                                        'categories': [place["searchResultBusiness"]["categories"][i]["title"] for i in range(len(place["searchResultBusiness"]["categories"]))],
                                        'thumbnail_img': place["scrollablePhotos"]["photoList"][0]["src"]
                                        }

    else:
        for r in all_results.keys():
            if 'searchExceptionProps' in all_results[r]['searchPageProps'].keys() or aliases == []:
                isValid = False

            else:
                isValid = True
                #print(all_results[r]["pageTitle"].split(" - ")[0])
                #locTitle = all_results[r]["pageTitle"].split(" - ")[0]
                search_results = all_results[r]['searchPageProps']['mainContentComponentsListProps']
                for place in search_results:
                    if place['searchResultLayoutType'] == "iaResult":
                        for i in range(len(place["searchResultBusiness"]["categories"])):
                            for a in aliases:
                                if a in place["searchResultBusiness"]["categories"][i]["title"].lower():
                                    tmp_data[place['searchResultBusiness']['name']] = {
                                        'name': place['searchResultBusiness']['name'],
                                        'rating': place['searchResultBusiness']['rating'],
                                        'reviewCount': place['searchResultBusiness']['reviewCount'],
                                        'url': "https://www.yelp.com" + place["searchResultBusiness"]["businessUrl"],
                                        'phone_num': place['searchResultBusiness']['phone'],
                                        'categories': [place["searchResultBusiness"]["categories"][i]["title"] for i in range(len(place["searchResultBusiness"]["categories"]))],
                                        'thumbnail_img': place["scrollablePhotos"]["photoList"][0]["src"]
                                        }
    return tmp_data, isValid, locTitle


x, y, z = getCache("Farmington", "hotel")
print(z)