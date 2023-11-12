CREATE TABLE users (
    id UUID DEFAULT UUID(),
    name VARCHAR(31) NOT NULL,
    -- email VARCHAR(63), -- not needed atm
    upload_limit INT UNSIGNED, -- NULL is no limit
    -- AUTH STUFF
    PRIMARY KEY (id),
    CONSTRAINT check_positive_upload_limit
        CHECK (upload_limit > 0 OR upload_limit IS NULL)
);

CREATE TABLE files (
    id INT UNSIGNED AUTO_INCREMENT,
    uploader_id UUID,
    short_link VARCHAR(255),
    url VARCHAR(255),
    mime_type VARCHAR(31),
    expires DATETIME,
    privacy ENUM('public', 'share', 'private') DEFAULT 'public' NOT NULL,
    PRIMARY KEY (id),
    INDEX(uploader_id, mime_type),
    FOREIGN KEY (uploader_id) REFERENCES users(id)
);

CREATE TABLE permissions (
    file_id INT UNSIGNED,
    user_id UUID,
    permission ENUM('owner', 'view'),
    INDEX(file_id),
    INDEX(user_id),
    INDEX(user_id, permission),
    FOREIGN KEY (file_id) REFERENCES files(id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER add_owner_permissions
AFTER INSERT ON files
FOR EACH ROW
BEGIN
    INSERT INTO permissions
    VALUES (NEW.id, NEW.uploader_id, 'owner');
END;//

DELIMITER ;
