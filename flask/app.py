import mariadb
import os
import time


# allow the database to start
connected = False
timeout = 0.5
while not connected:
# try to connect to MariaDB
    try:
        conn = mariadb.connect(
            user=os.environ.get('MARIADB_USER'),
            password=os.environ.get('MARIADB_PASSWORD'),
            host="mariadb",
            port=3306,
            database="filefort"
        )
        connected = True
    except mariadb.Error as e:
        timeout = timeout * 2
        print(f"Error connecting to MariaDB Platform: {e}, retrying in {timeout} seconds")
        time.sleep(timeout)
        if timeout > 20:
           raise TimeoutError("Database connection timeout")
    # Get Cursor
cur = conn.cursor(dictionary=True)
