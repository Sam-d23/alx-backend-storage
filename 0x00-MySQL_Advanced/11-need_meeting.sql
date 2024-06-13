-- Ensure the table 'students' exists (structure might differ based on actual table)
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    score INT,
    last_meeting DATE
);

-- Drop the view if it already exists
DROP VIEW IF EXISTS need_meeting;

-- Create the view 'need_meeting'
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
  AND (last_meeting IS NULL OR last_meeting < DATE_SUB(NOW(), INTERVAL 1 MONTH));

