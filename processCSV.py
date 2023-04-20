from pathlib import Path
import csv
import cache


def read_csv(filepath, encoding="utf-8-sig"):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a
    list of lists, wherein each nested list represents a single row from the
    input file.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file

    Returns:
        data (list): list of nested "row" lists
    """
    data = []
    with open(filepath, "r", encoding=encoding) as file_obj:
        reader = csv.reader(file_obj)
        for row in reader:
            data.append(row)
        return data

# TODO construct an absolute path
parent_path = Path(__file__).resolve().parent
states_path = parent_path.joinpath("US_States.csv")
cities_path = parent_path.joinpath("US_Cities.csv")

# TODO call function
usStates = read_csv(states_path)[1:]
usCities = read_csv(cities_path)[1:]

# format cities
cleanedCities = []
for i in usCities:
    cleanedCities.append([i[1], i[3]])

cleanedCities.sort(key = lambda x: x[1])

# format states
cleanedStates = []
for i in usStates:
    cleanedStates.append(i[0])

state_Cities = {}
for state in cleanedStates:
    state_Cities[state] = {'cities': []}

for i in cleanedCities:
    for state in cleanedStates:
        if i[1] == state:
            state_Cities[state]['cities'].append(i[0])

states = list(state_Cities.keys())

# load from cache or create cache
if cache.checkCacheExistence("state_city_names.json") == False:
    cache.save_cache(state_Cities, "state_city_names.json")
else:
    state_city_list = cache.checkCacheExistence("state_city_names.json")

# load from cache or create cache
if cache.checkCacheExistence("state_names.json") == False:
    cache.save_cache(state_Cities, "state_names.json")
else:
    state_list = cache.checkCacheExistence("state_names.json")

# load from cache or create cache
if cache.checkCacheExistence("All_US_States.json") == False:
    cache.save_cache(states, "All_US_States.json")
else:
    cities_list = cache.checkCacheExistence("All_US_States.json")
