import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    print((str(i + 1) + "/" + str(films.count()[1])), item['Name'], item['Year'])
    try:
        film = omdb(item)
    except ValueError:
        pass
    filmData = filmData.append(film, ignore_index=False)

# create language graphs

language = filmData.Language
language = language.str.split(', ', expand=True)
lingua = language[0].value_counts().to_frame()
lingua = lingua.reset_index(level = 0)
lingua.columns = ['language', 'frequency']

lingua.plot(x='language', y='frequency', kind='bar')
plt.show()

# create graphs of genre
genre = filmData.Genre.str.split(', ', expand=True)
genre = genre.fillna(value=np.nan)
genre = genre.apply(pd.value_counts, axis=0)
genre = genre.apply(np.sum, axis = 1)
genre.plot(kind='bar')
plt.show()
plt.show
