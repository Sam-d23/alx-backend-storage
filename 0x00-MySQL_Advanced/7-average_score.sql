-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create the projects table
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create the corrections table
CREATE TABLE IF NOT EXISTS corrections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    project_id INT,
    score INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Create the average_scores table
CREATE TABLE IF NOT EXISTS average_scores (
    user_id INT PRIMARY KEY,
    avg_score DECIMAL(5,2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the ComputeAverageScoreForUser stored procedure
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(5,2);

    -- Compute the average score for the given user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Insert or update the average score in the average_scores table
    INSERT INTO average_scores (user_id, avg_score)
    VALUES (user_id, avg_score)
    ON DUPLICATE KEY UPDATE avg_score = VALUES(avg_score);
END $$

DELIMITER ;
