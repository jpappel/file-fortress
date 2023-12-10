INSERT INTO users (name, upload_limit, collection_limit, collection_size_limt)
VALUES ("system",  NULL, NULL, NULL);

SELECT id INTO @system FROM users WHERE name = "system";

INSERT INTO files(uploader_id, short_link, url, mime_type)
VALUES (@system, "logo", "logo.png", "image/png"), (@system, "hello", "hello_world.txt", "text/plain");
