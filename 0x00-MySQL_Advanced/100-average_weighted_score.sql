-- SQL script that creates a stored procedure
--ComputeAverageWeightedScoreForUser that computes
--and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Change delimiter to allow semicolons inside the procedure
DELIMITER $$

-- Create the ComputeAverageWeightedScoreForUser procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE total_weighted_score DECIMAL(10,2) DEFAULT 0.0;
    DECLARE total_weight DECIMAL(10,2) DEFAULT 0.0;

    -- Calculate total weighted score
    SELECT SUM(corrections.score * projects.weight)
        INTO total_weighted_score
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    -- Calculate total weight
    SELECT SUM(projects.weight)
        INTO total_weight
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    -- Update average_score in users table based on total_weighted_score and total_weight
    IF total_weight = 0 THEN
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    ELSE
        UPDATE users
        SET average_score = total_weighted_score / total_weight
        WHERE id = user_id;
    END IF;
END $$

-- Reset the delimiter back to semicolon
DELIMITER ;
