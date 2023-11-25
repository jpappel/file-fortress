DELIMITER //

CREATE OR REPLACE PROCEDURE RemoveExpiredFiles (IN p_expire_date DATETIME, OUT p_remove_count INT)
BEGIN
    DECLARE v_error_message VARCHAR(255);
    DECLARE exit_handler BOOLEAN DEFAULT FALSE;

    -- Declare the handler for SQL exceptions
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET exit_handler = TRUE;

    START TRANSACTION;

    DELETE FROM files
    WHERE expires < p_expire_date;

    -- Get the number of rows deleted
    SELECT ROW_COUNT() INTO p_remove_count;

    IF NOT exit_handler THEN
        COMMIT;
    ELSE
        ROLLBACK;
        -- Log the error
        SELECT CONCAT('Error in RemoveExpired procedure: ', ERROR_MESSAGE()) INTO v_error_message;
    END IF;
END;
//

CREATE OR REPLACE PROCEDURE RemoveExpiredCollections (IN p_expire_date DATETIME, OUT p_remove_count INT)
BEGIN
    DECLARE v_error_message VARCHAR(255);
    DECLARE exit_handler BOOLEAN DEFAULT FALSE;

    -- Declare the handler for SQL exceptions
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET exit_handler = TRUE;

    START TRANSACTION;

    DELETE FROM collections
    WHERE expires < p_expire_date;

    -- Get the number of rows deleted
    SELECT ROW_COUNT() INTO p_remove_count;

    IF NOT exit_handler THEN
        COMMIT;
    ELSE
        ROLLBACK;
        -- Log the error
        SELECT CONCAT('Error in RemoveExpired procedure: ', ERROR_MESSAGE()) INTO v_error_message;
    END IF;
END;
//

DELIMITER ;
