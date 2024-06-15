-- Creates a function SafeDiv that divides (and returns) the first
-- by the second number or returns 0 if the second number is equal to 0.
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$

-- Function: SafeDiv
-- Description: Divides the first number by the second number or returns 0 if the second number is 0.
-- Parameters:
-- IN a INT: The numerator.
-- IN b INT: The denominator.
-- Returns: FLOAT - The result of the division or 0 if the denominator is 0.

CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    -- Declare result variable
    DECLARE result FLOAT;

    -- Check if the denominator is zero
    IF b = 0 THEN
        -- If denominator is zero, set result to 0
        SET result = 0;
    ELSE
        -- Otherwise, perform the division
        SET result = a / b;
    END IF;

    -- Return the result
    RETURN result;
END $$

DELIMITER ;

