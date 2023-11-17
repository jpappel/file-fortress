from .db import get_db

def get_file(short_link):
    db = get_db().cursor()
    db.execute("SELECT * FROM files WHERE short_link=%s", (short_link,))
    file = db.fetchone()
    if not file:
        return None
    return file
