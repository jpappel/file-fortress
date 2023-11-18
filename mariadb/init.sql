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
    modified_date DATETIME DEFAULT NOW() ON UPDATE NOW(),
    created_date DATETIME DEFAULT NOW(),
    PRIMARY KEY (id),
    INDEX idx_uploader_mime (uploader_id, mime_type),
    INDEX idx_modified_date (modified_date, id),
    INDEX idx_create_date (created_date, id),
    FOREIGN KEY (uploader_id) REFERENCES users(id)
);

CREATE TABLE permissions (
    file_id INT UNSIGNED,
    user_id UUID,
    permission ENUM('owner', 'viewer'),
    INDEX idx_file (file_id),
    INDEX idx_user (user_id),
    INDEX idx_user_permission (user_id, permission),
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
