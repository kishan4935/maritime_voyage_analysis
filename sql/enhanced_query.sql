WITH voyage_data AS (
    SELECT
        id,
        event,
        DATE_ADD('1899-12-30', INTERVAL dateStamp DAY) + INTERVAL timeStamp * 24 HOUR AS event_time,
        voyage_From,
        lat,
        lon,
        imo_num,
        voyage_Id,
        LAG(event) OVER (PARTITION BY voyage_Id ORDER BY event_time) AS prev_event,
        LAG(DATE_ADD('1899-12-30', INTERVAL dateStamp DAY) + INTERVAL timeStamp * 24 HOUR) OVER (PARTITION BY voyage_Id ORDER BY event_time) AS prev_event_time,
        LAG(lat) OVER (PARTITION BY voyage_Id ORDER BY event_time) AS prev_lat,
        LAG(lon) OVER (PARTITION BY voyage_Id ORDER BY event_time) AS prev_lon
    FROM voyages
    WHERE allocatedVoyageId IS NULL AND imo_num = '9434761' AND voyage_Id = '6'
),
distance_calc AS (
    SELECT
        id,
        event,
        event_time,
        voyage_From,
        lat,
        lon,
        imo_num,
        voyage_Id,
        prev_event,
        prev_event_time,
        TIMESTAMPDIFF(MINUTE, prev_event_time, event_time) / 60.0 AS time_diff_hours,
        3959 * ACOS(
            COS(RADIANS(lat)) * COS(RADIANS(prev_lat)) *
            COS(RADIANS(prev_lon) - RADIANS(lon)) +
            SIN(RADIANS(lat)) * SIN(RADIANS(prev_lat))
        ) AS distance_travelled
    FROM voyage_data
)
SELECT
    id,
    event,
    event_time,
    voyage_From,
    lat,
    lon,
    imo_num,
    voyage_Id,
    prev_event,
    prev_event_time,
    time_diff_hours,
    distance_travelled,
    CASE
        WHEN event = 'SOSP' THEN time_diff_hours
        ELSE NULL
    END AS sailing_time,
    CASE
        WHEN event = 'EOSP' THEN time_diff_hours
        ELSE NULL
    END AS port_stay_duration
FROM distance_calc
ORDER BY event_time;
