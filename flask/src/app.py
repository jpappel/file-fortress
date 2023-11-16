from flask import Flask


app = Flask(__name__, template_folder="../templates", static_folder="../static")


from file_routes import *
from website_routes import *
