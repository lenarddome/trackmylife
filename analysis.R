library(data.table)
library(ggplot2)
library(cowplot)

films <- fread("films.csv")

linguafrance <- sapply(films$Language, function (x) strsplit(x, ", "),
                       USE.NAMES = FALSE)
linguafrance <- type.convert(sapply(linguafrance, "[[", 1))

ggplot() +
    geom_histogram(mapping = aes(x = linguafrance), stat = "count") +
    theme_cowplot() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

countries <- sapply(films$Country, function (x) strsplit(x, ", "),
                    USE.NAMES = FALSE)
countries <- type.convert(matrix(unlist(countries, use.names = FALSE)))

ggplot() +
    geom_histogram(mapping = aes(x = countries), stat = "count") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

genre <- sapply(films$Genre, function (x) strsplit(x, ", "),
                    USE.NAMES = FALSE)
genre <- type.convert(matrix(unlist(genre, use.names = FALSE)))

ggplot() +
    geom_histogram(mapping = aes(x = genre), stat = "count") +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
