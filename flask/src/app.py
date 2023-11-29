from flask import Flask
from .db import get_db
from .file_routes import file_api
from .website_routes import website
from .StorageManagers import LocalStorageManager


app = Flask(__name__, template_folder="./templates", static_folder="./static")

# create database sessionn
db = get_db()
app.config['db'] = db

# create storage manager
storage_root = '/mnt/file_storage'
app.config['storage_manager'] = LocalStorageManager(db, storage_root)

# register blueprints
app.register_blueprint(file_api)
app.register_blueprint(website)
