CREATE TABLE IF NOT EXISTS clicks_by_geo
(
    link_id UUID,
    geo String,
    clicks_count AggregateFunction(count, UInt32)
)
ENGINE = AggregatingMergeTree
PARTITION BY link_id
ORDER BY (link_id, geo);

CREATE MATERIALIZED VIEW IF NOT EXISTS clicks_by_geo_mv
TO clicks_by_geo
AS
SELECT
    link_id,
    geo,
    countState(*) AS clicks_count
FROM click_stamp
GROUP BY link_id, geo;