--Ranks country origins of bands
CREATE TEMPORARY TABLE country_fan_counts AS
SELECT origin, SUM(nb_fans) AS total_fans
FROM metal_bands
GROUP BY origin;
