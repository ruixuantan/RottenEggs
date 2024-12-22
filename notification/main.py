import json
import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, List, Optional

import dotenv
import pydantic
from cassandra.cluster import Cluster
from fastapi import FastAPI
from pydantic import BaseModel

dotenv.load_dotenv()
cluster = Cluster([os.getenv("DB_HOST")], port=os.getenv("DB_PORT"))
session = cluster.connect(os.getenv("KEYSPACE_NAME"))
subscribers = []


class Message(BaseModel):
    id: int
    budget: int
    homepage: str
    original_language: str
    popularity: float
    release_date: str
    revenue: int
    runtime: int
    status: str
    stars: int
    review: str
    genres: List[int]


@pydantic.dataclasses.dataclass
class Preference:
    dimension: str
    contains: Optional[Any] = None
    lt: Optional[Any] = None
    gt: Optional[Any] = None

    def to_notify(self, msg: Message) -> bool:
        dim = msg.__dict__[self.dimension]
        if self.contains:
            return all(elem in dim for elem in self.contains)
        elif self.lt and self.gt:
            return self.lt <= dim <= self.gt
        else:
            return False


@dataclass(frozen=True)
class Subscriber:
    topic_name: str
    preferences: List[Preference]

    def to_notify(self, msg: Message) -> bool:
        return all(preference.to_notify(msg) for preference in self.preferences)


@asynccontextmanager
async def lifespan(app: FastAPI):
    rows = session.execute("SELECT * FROM subscribers")
    for row in rows:
        preferences = [Preference(**p) for p in json.loads(row.preferences.decode("utf-8"))["preferences"]]
        subscribers.append(Subscriber(topic_name=row.kafka_topic, preferences=preferences))
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/notifications")
async def create_notification(message: Message):
    # TODO: convert to async
    for subscriber in subscribers:
        if subscriber.to_notify(message):
            # TODO: send kafka message
            print(subscriber, message)
    return {"status": "ok"}


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
