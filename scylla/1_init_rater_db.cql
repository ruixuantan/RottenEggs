CREATE KEYSPACE IF NOT EXISTS rater WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

DROP TABLE IF EXISTS rater.movies;
DROP TABLE IF EXISTS rater.genres;
DROP TABLE IF EXISTS rater.movie_genres;
DROP TABLE IF EXISTS rater.ratings;


CREATE TABLE IF NOT EXISTS rater.movies (
    id int,
    budget bigint,
    homepage text,
    original_language text,
    original_title blob,
    release_date date,
    status text,
    overview blob,
    tagline blob,
    title blob,
    popularity double,
    revenue bigint,
    runtime int,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS rater.genres (
    id int,
    name text,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS rater.movie_genres (
    movie_id int,
    genre_id int,
    PRIMARY KEY (movie_id, genre_id)
) WITH CLUSTERING ORDER BY (genre_id ASC);

CREATE TABLE IF NOT EXISTS rater.ratings (
    id uuid,
    movie_id int,
    stars tinyint,
    review text,
    timestamp timestamp,
    PRIMARY KEY (id, movie_id)
) WITH CLUSTERING ORDER BY (movie_id ASC);

COPY rater.genres FROM 'scripts/genres.csv' WITH HEADER = true;
COPY rater.movie_genres FROM 'scripts/movie_genres.csv' WITH HEADER = true;
