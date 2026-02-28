CREATE TABLE IF NOT EXISTS clicks_by_client
(
    link_id UUID,
    platform String,
    client String,
    clicks_count AggregateFunction(count, UInt32)
)
ENGINE = AggregatingMergeTree
PARTITION BY link_id
ORDER BY (link_id, platform, client);

CREATE MATERIALIZED VIEW IF NOT EXISTS clicks_by_client_mv
TO clicks_by_client
AS
SELECT
    link_id,
    platform,
    client,
    countState(*) AS clicks_count
FROM click_stamp
GROUP BY link_id, platform, client;