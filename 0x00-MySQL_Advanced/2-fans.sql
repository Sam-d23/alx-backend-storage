-- SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans.
-- This script assumes the table is imported from metal_bands.sql.zip and the table name is metal_bands

-- Rank country origins by the number of fans
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;

