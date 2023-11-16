from db import get_db

def get_file(short_link):
    db = get_db()
    db.execute("SELECT * FROM files WHERE short_link=?", (short_link,))
    file = db.fetchone()
    if not file:
        return None
    return file

