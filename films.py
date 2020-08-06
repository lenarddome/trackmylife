import requests
import pandas as pd

# import movie list
films = []
films = pd.read_csv("data/films_seen.csv")

def omdb(string):
    '''Takes an object with variables Name and Year to fetch movie data'''
    baseurl = "http://www.omdbapi.com/"
    name = {}
    name['apikey'] = "aa45416f"
    name['t'] = string['Name']
    name['y'] = int(string['Year'])
    name['r'] = 'json'
    final = requests.get(baseurl, params=name)
    output = final.json()
    output = pd.json_normalize(output)
    return output

# create empty dataframe for move data
filmData = pd.DataFrame(columns=[25])

# create data for 
for i in range(0, films.count()[1]):
    item = films.iloc[i][['Name', 'Year']]
    print(i, item['Name'], item['Year'])
    try:
        film = omdb(item)
    except ValueError:
        pass
    filmData = filmData.append(film, ignore_index=False)
