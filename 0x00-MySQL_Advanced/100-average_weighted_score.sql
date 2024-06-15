-- Task: Create a stored procedure ComputeAverageWeightedScoreForUser that computes and stores the average weighted score for a student

DELIMITER //

-- Stored Procedure: ComputeAverageWeightedScoreForUser
-- Description: Computes and stores the average weighted score for a student based on the scores and weights in the 'scores' table.
-- Parameters:
-- IN user_id INT: The ID of the user for whom the average weighted score is to be computed.
-- Assumptions:
-- 1. The 'scores' table has columns 'user_id', 'score', and 'weight'.
-- 2. The 'users' table has a column 'average_weighted_score' to store the computed average.

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weighted_score DECIMAL(10, 2);
    DECLARE total_weight DECIMAL(10, 2);
    DECLARE average_weighted_score DECIMAL(10, 2);

    -- Calculate the total weighted score and total weight for the given user_id
    SELECT SUM(score * weight), SUM(weight) 
    INTO total_weighted_score, total_weight
    FROM scores
    WHERE user_id = user_id;

    -- Compute the average weighted score
    SET average_weighted_score = total_weighted_score / total_weight;

    -- Update the user's average weighted score in the users table
    UPDATE users
    SET average_weighted_score = average_weighted_score
    WHERE id = user_id;
END //

DELIMITER ;

