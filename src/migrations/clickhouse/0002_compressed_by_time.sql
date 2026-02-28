CREATE TABLE IF NOT EXISTS clicks_by_date
(
    link_id UUID,
    date Date,
    hour UInt8,
    clicks_count AggregateFunction(count, UInt32)
)
ENGINE = AggregatingMergeTree
PARTITION BY toYYYYMM(date)
ORDER BY (link_id, date, hour);

CREATE MATERIALIZED VIEW IF NOT EXISTS clicks_by_date_mv
TO clicks_by_date
AS
SELECT
    link_id,
    toDate(timestamp) AS date,
    toHour(timestamp) AS hour,
    countState(*) AS clicks_count
FROM click_stamp
GROUP BY
    link_id, date, hour;