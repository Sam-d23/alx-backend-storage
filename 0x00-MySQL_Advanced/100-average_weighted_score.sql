-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Change delimiter to define the stored procedure
DELIMITER $$

-- Create the ComputeAverageWeightedScoreForUser stored procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE sum_scores DECIMAL(10,2);
    DECLARE total_weight DECIMAL(10,2);

    -- Calculate the sum of scores weighted by project importance
    SELECT SUM(s.score * p.importance) INTO sum_scores, SUM(p.importance) INTO total_weight
    FROM scores s
    JOIN projects p ON s.project_id = p.id
    WHERE s.user_id = user_id;

    -- Calculate the average weighted score
    DECLARE avg_weighted_score DECIMAL(5,2);
    IF total_weight > 0 THEN
        SET avg_weighted_score = sum_scores / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;

    -- Insert or update the average weighted score in the average_weighted_scores table
    INSERT INTO average_weighted_scores (user_id, avg_weighted_score)
    VALUES (user_id, avg_weighted_score)
    ON DUPLICATE KEY UPDATE avg_weighted_score = avg_weighted_score;
END $$

-- Reset delimiter to default
DELIMITER ;

