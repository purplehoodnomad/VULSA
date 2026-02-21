CREATE TABLE IF NOT EXISTS click_stamp
(
    id UUID,
    link_id UUID,
    short String,
    timestamp DateTime,

    ip String,
    user_agent String,
    referer String,
    request_url String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(timestamp)
ORDER BY (link_id, timestamp, id)