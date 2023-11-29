from flask import Flask
from .db import get_db
from .file_routes import file_api
from .website_routes import website
from .StorageManagers import LocalStorageManager
from .configurations import ProductionConfig



def create_app(config=None) -> Flask:
    app = Flask(__name__, template_folder="./templates", static_folder="./static")

    if config is None:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(config)

    # register blueprints
    app.register_blueprint(file_api)
    app.register_blueprint(website)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
