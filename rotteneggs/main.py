import datetime
import os
import uuid

import dotenv
from cassandra.cluster import Cluster
from fastapi import FastAPI
from pydantic import BaseModel

dotenv.load_dotenv()
cluster = Cluster([os.getenv("DB_HOST")], port=os.getenv("DB_PORT"))
session = cluster.connect(os.getenv("KEYSPACE_NAME"))
app = FastAPI()


class Ratings(BaseModel):
    movie_id: int
    stars: int
    review: str


@app.post("/ratings")
async def create_rating(rating: Ratings):
    id = uuid.uuid4().hex
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    session.execute(
        f"""
        INSERT INTO ratings (id, movie_id, stars, review, timestamp)
        VALUES ('{id}', {rating.movie_id}, {rating.stars}, '{rating.review}', '{timestamp}')
        """
    )
    return {"status": "ok"}


@app.get("/movies")
async def get_movie_ids():
    rows = session.execute("SELECT id FROM movies")
    ids = [row.id for row in rows]
    return {"ids": ids}


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
