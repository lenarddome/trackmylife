# load packages
library(data.table)
library(httr)
library(jsonlite)
library(RCurl)
library(dplyr)

# function to get info about films using Open Movie Database
# this is my personal patron API key, please request your own!
# Consider supporting the Open Movie Database! http://www.omdbapi.com/
watched_API <- function(title, year) {
    titleURL <- curlEscape(title)
    url <- "http://www.omdbapi.com/?"
    film <- GET(paste(url, "t=", titleURL, "&y=", year, "&apikey=aa45416f&", sep = ""))
    contentdf <- do.call(what = "rbind",
                         lapply(rawToChar(film$content), as.data.frame))
    # convert json to data frame
    prep <- fromJSON(as.character(contentdf[1, 1]))
    prep$Ratings <- NULL
    return(data.frame(prep))
}


# TODO: function to retrieve info of books via ISBN


# import watched film list
watched <- fread("films_seen.csv")
pb = txtProgressBar(min = 0, max = nrow(watched), initial = 0)
films <- NULL
state = 0

for (i in seq_len(nrow(watched))) {
    state = state + 1
    setTxtProgressBar(pb, state)
    x <- watched[i, 2:3]
    finfo <- watched_API(x[1, 1], x[1, 2])
    films <- bind_rows(films, finfo)
}

#films <- do.call(bind_rows,
#                 apply(watched[1:100, 2:3], 1,
#                       function(x) watched_API(x[1], x[2])))

films <- cbind(watched[, 1], films)
films <- as.data.table(films)

write.csv(films, "../films.csv")
