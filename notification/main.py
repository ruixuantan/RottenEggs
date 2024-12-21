import os

import dotenv
from cassandra.cluster import Cluster
from fastapi import FastAPI

dotenv.load_dotenv()
cluster = Cluster([os.getenv("DB_HOST")], port=os.getenv("DB_PORT"))
session = cluster.connect(os.getenv("KEYSPACE_NAME"))
app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
