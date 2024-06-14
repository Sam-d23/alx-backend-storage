-- SQL script to create a function SafeDiv
-- The function divides the first number by the second number
-- and returns 0 if the second number is equal to 0

DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS DECIMAL(10, 2)
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END $$

DELIMITER ;
