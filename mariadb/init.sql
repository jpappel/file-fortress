CREATE TABLE users (
    id UUID DEFAULT UUID(),
    name VARCHAR(32) NOT NULL,
    -- email VARCHAR(63), -- not needed atm
    upload_limit INT UNSIGNED, -- NULL is no limit
    collection_limit INT UNSIGNED DEFAULT 32,
    collection_size_limit INT UNSIGNED DEFAULT 16,
    -- AUTH STUFF
    username VARCHAR(32) UNIQUE NOT NULL,
    hash VARCHAR(128) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT check_positive_upload_limit
        CHECK (upload_limit > 0 OR upload_limit IS NULL),
    CONSTRAINT check_positive_collection_limit
        CHECK (collection_limit > 0 OR collection_limit IS NULL),
    CONSTRAINT check_positive_collection_size_limit
        CHECK (collection_size_limit > 0 OR collection_size_limit IS NULL)
);

CREATE TABLE files (
    id INT UNSIGNED AUTO_INCREMENT,
    uploader_id UUID,
    short_link VARCHAR(256) UNIQUE NOT NULL,
    url VARCHAR(256),
    mime_type VARCHAR(32),
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
    PRIMARY KEY (file_id, user_id),
    INDEX idx_file (file_id),
    INDEX idx_user (user_id),
    INDEX idx_user_permission (user_id, permission),
    FOREIGN KEY (file_id) REFERENCES files(id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE TABLE collections (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(256) NOT NULL,
    creator_id UUID,
    short_link VARCHAR(256) UNIQUE NOT NULL,
    url VARCHAR(256) NOT NULL,
    privacy ENUM('public', 'share', 'private') DEFAULT 'public' NOT NULL,
    expires DATETIME,
    modified_date DATETIME DEFAULT NOW() ON UPDATE NOW(),
    created_date DATETIME DEFAULT NOW() ON UPDATE NOW(),
    size_limit INT, -- COALESCE should be used when querying this column
    PRIMARY KEY (id),
    INDEX idx_id_creator (id, creator_id),
    FOREIGN KEY (creator_id) REFERENCES users(id)
);

CREATE TABLE collection_files (
    collection_id INT UNSIGNED,
    file_id INT UNSIGNED,
    FOREIGN KEY (collection_id) REFERENCES collections(id)
        ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES files(id)
        ON DELETE CASCADE
);

CREATE VIEW collection_size_info AS (
    SELECT
        i.id AS collection_id,
        COALESCE(i.size_limit, (SELECT collection_size_limit FROM users WHERE i.creator_id = users.id LIMIT 1)) AS size_limit,
        COALESCE(c.total_files, 0) AS total_files
    FROM
        (SELECT id, creator_id, size_limit FROM collections) i
    LEFT JOIN (
        SELECT collection_id, COUNT(*) AS total_files
        FROM collection_files
        GROUP BY collection_id
    ) c
    ON i.id = c.collection_id
);

CREATE TABLE collection_permissions (
    collection_id INT UNSIGNED,
    user_id UUID,
    permission ENUM('owner', 'editor', 'viewer'),
    PRIMARY KEY (collection_id, user_id),
    FOREIGN KEY (collection_id) REFERENCES collections(id)
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

CREATE TRIGGER collections_add_owner_permissions
AFTER INSERT ON collections
FOR EACH ROW
BEGIN
    INSERT INTO collection_permissions
    VALUES (NEW.id, NEW.creator_id, 'owner');
END;//

DELIMITER ;
