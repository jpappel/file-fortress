from flask import Flask, jsonify
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


app = Flask(__name__)


@app.route('/')
def main():
    return '<p>Flask works!</p>'
    # return render_template('index.html')


@app.route('/<short_link>', methods=['GET'])
def get_file(short_link):
    cur.execute("SELECT * FROM files WHERE short_link=?", (short_link,))
    file = cur.fetchone()
    if not file:
        return 'file not found', 404
    return jsonify(file)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
