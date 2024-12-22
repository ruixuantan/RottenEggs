import logging
import os
from contextlib import asynccontextmanager

import dotenv
import httpx
from cassandra.cluster import Cluster
from fastapi import FastAPI
from pydantic import BaseModel

logger = logging.getLogger("uvicorn.error")
dotenv.load_dotenv()
cluster = Cluster([os.getenv("DB_HOST")], port=os.getenv("DB_PORT"))
session = cluster.connect(os.getenv("KEYSPACE_NAME"))
notification_url = f"http://{os.getenv('NOTIFICATION_HOST')}:{os.getenv('NOTIFICATION_PORT')}"
prepared_stmts = {}


class Ratings(BaseModel):
    movie_id: int
    stars: int
    review: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()

    prepared_stmts["insert_ratings"] = session.prepare(
        """
        INSERT INTO ratings (id, movie_id, stars, review, timestamp) VALUES (uuid(),?,?,?,currentTimestamp())
    """
    )
    prepared_stmts["get_movie_by_id"] = session.prepare("SELECT * FROM movies WHERE id = ?")
    prepared_stmts["get_movie_genre_by_id"] = session.prepare("SELECT * FROM movie_genres WHERE movie_id = ?")

    yield
    await app.requests_client.aclose()


app = FastAPI(lifespan=lifespan)


@app.post("/ratings")
async def create_rating(rating: Ratings):
    session.execute(prepared_stmts["insert_ratings"], [rating.movie_id, rating.stars, rating.review])
    movie = session.execute(prepared_stmts["get_movie_by_id"], [rating.movie_id]).one()
    movie_genres = session.execute(prepared_stmts["get_movie_genre_by_id"], [rating.movie_id])
    movie_genres = [row.genre_id for row in movie_genres]

    ### for convenience ###
    payload = movie._asdict() | vars(rating)
    payload.pop("movie_id")
    byte_keys = []
    for k, v in payload.items():
        if isinstance(v, bytes):
            byte_keys.append(k)
    for k in byte_keys:
        payload.pop(k)
    payload["genres"] = movie_genres
    payload["release_date"] = payload["release_date"].date().strftime("%Y-%m-%d")
    ########################

    notification_response = await app.requests_client.post(f"{notification_url}/notifications", json=payload)
    if notification_response.status_code != httpx.codes.OK:
        # TODO: error retry
        logger.error(notification_response.json())
    return {"status": "ok"}


@app.get("/movies")
async def get_movie_ids():
    rows = session.execute("SELECT id FROM movies")
    ids = [row.id for row in rows]
    return {"ids": ids}


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
