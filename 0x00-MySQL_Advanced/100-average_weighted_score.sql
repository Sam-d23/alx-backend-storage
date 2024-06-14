-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- This procedure computes and stores the average weighted score for a student

-- Drop the procedure if it already exists to avoid errors
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score DECIMAL(10, 2) DEFAULT 0;
    DECLARE total_weight DECIMAL(10, 2) DEFAULT 0;
    DECLARE avg_weighted_score DECIMAL(10, 2) DEFAULT 0;

    -- Calculate the total weighted score for the user
    SELECT SUM(corrections.score * projects.weight)
    INTO total_weighted_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the total weight for the user
    SELECT SUM(projects.weight)
    INTO total_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the average weighted score
    IF total_weight != 0 THEN
        SET avg_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;

    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = avg_weighted_score
    WHERE id = user_id;
END $$

DELIMITER ;

