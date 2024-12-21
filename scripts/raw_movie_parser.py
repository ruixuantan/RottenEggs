import csv
import json
from typing import Any, Dict, Iterator, List

Row = Dict[str, Any]

PATH = "data/tmdb_5000_movies.csv"
MOVIES = []
MOVIE_HEADERS = [
    "id",
    "budget",
    "homepage",
    "original_language",
    "original_title",
    "release_date",
    "status",
    "overview",
    "tagline",
    "title",
    "popularity",
    "revenue",
    "runtime",
]
STR_MOVIE_HEADERS = [
    "homepage",
    "original_language",
    "release_date",
    "status",
]
BLOB_MOVIE_HEADERS = [
    "original_title",
    "overview",
    "tagline",
    "title",
]
MOVIES_PATH = "scylla/2_insert_movies.cql"

GENRES = []
GENRE_HEADERS = ["id", "name"]
GENRES_PATH = "scylla/genres.csv"
GENRE_IDS = set()

MOVIE_GENRES = []
MOVIE_GENRES_HEADERS = ["movie_id", "genre_id"]
MOVIE_GENRES_PATH = "scylla/movie_genres.csv"


def read_file(path: str = PATH) -> Iterator[Row]:
    with open(PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def process_row(row: Row) -> None:
    row["runtime"] = int(float(row["runtime"]) if row["runtime"] != "" else 0)
    MOVIES.append({key: row[key] for key in MOVIE_HEADERS})
    genres = json.loads(row["genres"])
    for genre in genres:
        if genre["id"] not in GENRE_IDS:
            GENRE_IDS.add(genre["id"])
            GENRES.append(genre)
        MOVIE_GENRES.append({"movie_id": row["id"], "genre_id": genre["id"]})


def write_file(path: str, header: List[str], table: List[Row]) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in table:
            writer.writerow(row)


def process_movie_row(row: Row) -> str:
    head = f"INSERT INTO rater.movies ({', '.join(MOVIE_HEADERS)}) VALUES "
    for k, v in row.items():
        if k in STR_MOVIE_HEADERS:
            row[k] = f"'{row[k]}'"
        elif k in BLOB_MOVIE_HEADERS:
            row[k] = "0x" + row[k].encode("utf-8").hex()
    return head + f"({', '.join([str(row[col]) for col in MOVIE_HEADERS])});\n"


def write_movie_insert_file() -> None:
    with open(MOVIES_PATH, "w") as f:
        f.write("USE rater;\n")
        for row in MOVIES:
            row_line = process_movie_row(row)
            f.write(row_line)


def main():
    for row in read_file():
        process_row(row)
    write_movie_insert_file()
    write_file(GENRES_PATH, GENRE_HEADERS, GENRES)
    write_file(MOVIE_GENRES_PATH, MOVIE_GENRES_HEADERS, MOVIE_GENRES)


if __name__ == "__main__":
    main()
