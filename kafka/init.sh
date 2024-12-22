#!/bin/bash

echo ${KAFKA_TOPICS}
topics=$(echo ${KAFKA_TOPICS} | tr "," "\n")

for topic in $topics
do
  kafka-topics.sh --bootstrap-server ${KAFKA_HOST}:${KAFKA_PORT} --delete --topic ${topic}
  kafka-topics.sh --bootstrap-server ${KAFKA_HOST}:${KAFKA_PORT} \
    --create --topic ${topic} --if-not-exists \
    --partitions 1 --replication-factor 1
done
kafka-topics.sh --bootstrap-server kafka:9092 --list
