CREATE KEYSPACE IF NOT EXISTS notification WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

DROP TABLE IF EXISTS notification.subscribers;

CREATE TABLE IF NOT EXISTS notification.subscribers (
    id uuid,
    name text,
    kafka_topic text,
    timestamp timestamp,
    preferences blob,
    PRIMARY KEY (id)
);

INSERT INTO notification.subscribers (id, name, kafka_topic, timestamp, preferences) VALUES
(uuid(), 'Documentary_Analytics_System', 'DocumentaryAnalyticsTopic', currentTimestamp(), textAsBlob('{"preferences": [{"dimension": "genres", "contains": [99]}]}'));

INSERT INTO notification.subscribers (id, name, kafka_topic, timestamp, preferences) VALUES
(uuid(), 'Indiefilm_Recommender_System', 'IndiefilmRecommenderTopic', currentTimestamp(), textAsBlob('{"preferences": [{"dimension": "revenue", "gt": 500000, "lt": 1000000}]}'));

INSERT INTO notification.subscribers (id, name, kafka_topic, timestamp, preferences) VALUES
(uuid(), 'Consume_All_System', 'ConsumeAllTopic', currentTimestamp(), textAsBlob('{"preferences": []}'));
