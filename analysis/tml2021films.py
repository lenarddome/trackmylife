import requests
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import imdb
from genderize import Genderize
ia = imdb.IMDb()

# import movie list
films = []
films = pd.read_csv("../data/movies/watched.csv")
watchlist = pd.read_csv("../data/movies/watchlist.csv")


def omdb(string):
    '''Takes an object with variables IMDB ID and Year to fetch movie data'''
    baseurl = "http://www.omdbapi.com/"
    name = {}
    name['apikey'] = "aa45416f"
    name['i'] = string['ID']
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
    print((str(i + 1) + "/" + str(films.count()[1])),
          item['Name'], int(item['Year']))
    imdbID = ia.search_movie(item['Name'])[0].movieID
    try:
        film = omdb({'ID': "tt" + imdbID, 'Year': item['Year']})
        filmData = filmData.append(film, ignore_index=False)
    except ValueError:
        pass
    if not pd.isna(film['Title'])[0]:
        print('Found.')
    else:
        print('Not found.')

# create language graphs

language = filmData.Language
language = language.str.split(', ', expand=True)
lingua = language[0].value_counts().to_frame()
lingua = lingua.reset_index(level=0)
lingua.columns = ['language', 'frequency']

lingua.plot(x='language', y='frequency', kind='bar')
plt.show()

# create graphs of genre
genre = filmData.Genre.str.split(', ', expand=True)
genre = genre.fillna(value=np.nan)
genre = genre.apply(pd.value_counts, axis=0)
genre = genre.apply(np.sum, axis=1)
genre.plot(kind='bar')
plt.show()

film_year = filmData.groupby(by='Year')['Year'].count().reset_index(name='cnt')
film_year.plot(x='Year', y='cnt', kind='bar')
plt.show()

films2017 = filmData[filmData["Year"] == "2017"]
films2017['Runtime'].str.extract('(\d+)').astype(float).plot(kind='hist')
plt.show()

pd.set_option('display.max_rows', None)
pd.reset_option('display.max_rows')

directors = filmData['Director']
directors = pd.Series(directors.str.split(expand=True).iloc[:, 0].unique())
big_gender = pd.DataFrame()

for i in range(0, directors.count()):
    try:
        names = directors.iloc[i].split()[0]
        gender = Genderize().get([names])
        big_gender.append(pd.json_normalize(gender), ignore_index=False)
        print((str(i + 1) + "/" + str(directors.count())),
              directors.iloc[i].split(), gender)
    except ValueError:
        pass
