-- Create the names table if it does not exist
CREATE TABLE IF NOT EXISTS names (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    score INT
);

-- Create the index on the first letter of the name column and score
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
