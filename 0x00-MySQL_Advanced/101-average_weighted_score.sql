-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Change delimiter to allow semicolons inside the procedure
DELIMITER $$

-- Create the ComputeAverageWeightedScoreForUsers procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_weighted_score DECIMAL(10,2);
    DECLARE total_weight DECIMAL(10,2);
    DECLARE avg_weighted_score DECIMAL(10,2);
    
    -- Cursor to iterate over each user
    DECLARE cur CURSOR FOR
        SELECT id
        FROM users;
    
    -- Handlers for cursor operations
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Calculate total weighted score
        SELECT COALESCE(SUM(corrections.score * projects.weight), 0)
            INTO total_weighted_score
            FROM corrections
            INNER JOIN projects ON corrections.project_id = projects.id
            WHERE corrections.user_id = user_id;
        
        -- Calculate total weight
        SELECT COALESCE(SUM(projects.weight), 0)
            INTO total_weight
            FROM corrections
            INNER JOIN projects ON corrections.project_id = projects.id
            WHERE corrections.user_id = user_id;
        
        -- Calculate average weighted score
        IF total_weight > 0 THEN
            SET avg_weighted_score = total_weighted_score / total_weight;
        ELSE
            SET avg_weighted_score = 0;
        END IF;
        
        -- Update average_score in users table
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id;
    END LOOP;
    
    CLOSE cur;
END $$

-- Reset the delimiter back to semicolon
DELIMITER ;

