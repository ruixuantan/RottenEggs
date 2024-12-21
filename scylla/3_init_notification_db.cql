CREATE KEYSPACE IF NOT EXISTS notification WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

DROP TABLE IF EXISTS notification.subscribers;

CREATE TABLE IF NOT EXISTS notification.subscribers (
    id uuid,
    name text,
    timestamp timestamp,
    preferences blob,
    PRIMARY KEY (id)
);

INSERT INTO notification.subscribers (id, name, timestamp, preferences) VALUES
(uuid(), 'Documentary_Analytics_System', currentTimestamp(), textAsBlob('{"preferences": [{"dimension": "genre", "contains": [99]}]}'));

INSERT INTO notification.subscribers (id, name, timestamp, preferences) VALUES
(uuid(), 'Indiefilm_Recommnder_System', currentTimestamp(), textAsBlob('{"preferences": [{"dimension": "revenue", "gt": 500000, "lt": 1000000}]}'));
