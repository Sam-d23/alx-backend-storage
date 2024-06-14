-- SQL script that creates a function SafeDiv
-- This function divides the first argument by the second or returns 0 if the second argument is 0

-- Drop the function if it already exists to avoid errors
DROP FUNCTION IF EXISTS SafeDiv;

-- Create the SafeDiv function
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    -- Check if the divisor is 0
    IF b = 0 THEN
        -- Return 0 if the divisor is 0
        RETURN 0;
    ELSE
        -- Otherwise, return the result of the division
        RETURN a / b;
    END IF;
END $$

DELIMITER ;
