import argparse
import logging
import os
import time

import requests
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient

logging.basicConfig(level=logging.INFO)
kafka_url = f"{os.getenv('KAFKA_HOST')}:{os.getenv('KAFKA_PORT')}"
downstream_url = (
    f"http://{os.getenv('DOWNSTREAM_HOST')}:{os.getenv('DOWNSTREAM_PORT')}/{os.getenv('DOWNSTREAM_RESOURCE')}"
)


def connect_topic(kafka_topic: str):
    admin = AdminClient({"bootstrap.servers": kafka_url})
    topics = list(admin.list_topics().topics.keys())
    while kafka_topic not in topics:
        time.sleep(1)
        topics = list(admin.list_topics().topics.keys())
    kafka.subscribe([kafka_topic])
    logging.info(f"Connected to kafka topic: {kafka_topic}")


def consume(kafka: Consumer, interval: float):
    try:
        while True:
            msg = kafka.poll(interval)
            if msg is None:
                continue
            elif msg.error():
                logging.error(msg.error())
            else:
                logging.info(msg.value().decode("utf-8"))
                # TODO: error retry
                requests.post(downstream_url, json=msg.value().decode("utf-8"))
    finally:
        kafka.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        help="Group id of consumer.",
    )
    parser.add_argument(
        "-t",
        "--topic",
        type=str,
        help="Topic name to consume from.",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        help="Rate at which messages are consumed from",
        default=1.0,
    )
    kafka = Consumer(
        {
            "bootstrap.servers": kafka_url,
            "group.id": f"{parser.parse_args().group}",
            "auto.offset.reset": "earliest",
            "enable.auto.offset.store": False,
        }
    )
    connect_topic(parser.parse_args().topic)
    consume(kafka, parser.parse_args().interval)
