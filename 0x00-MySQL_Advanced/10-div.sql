--SQL script that creates a function SafeDiv
--that divides (and returns) the first by the
--second number or returns 0 if the second
--number is equal to 0.
DROP FUNCTION IF EXISTS SafeDiv;

-- Create the SafeDiv function
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS INT
BEGIN
    DECLARE result INT;

    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = a / b;
    END IF;

    RETURN result;
END;