-- Ensure the trigger doesn't already exist
DROP TRIGGER IF EXISTS reset_valid_email;

-- Change delimiter to define the trigger
DELIMITER $$

-- Create the trigger to reset valid_email when email is changed
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = FALSE;
    END IF;
END $$

-- Reset delimiter to default
DELIMITER ;
