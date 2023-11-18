from flask import Flask


app = Flask(__name__, template_folder="./templates", static_folder="./static")


from . import file_routes
from . import website_routes
