from flask import Flask
from .db import get_db
from .file_routes import file_api
from .website_routes import website


app = Flask(__name__, template_folder="./templates", static_folder="./static")

# create database sessionn
app.config['db'] = get_db()

# register blueprints
app.register_blueprint(file_api)
app.register_blueprint(website)
