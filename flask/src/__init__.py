from flask import Flask
from src.file_routes import file_api, file_view
from src.website_routes import website
from src.users import users, login_manager
from src.configurations import Config


def create_app(config: Config = None) -> Flask:
    app = Flask(__name__, template_folder="./templates", static_folder="./static")

    if config is None:
        from src.configurations import production_config
        app.config.from_object(production_config())
    else:
        app.config.from_object(config)

    # init login manager
    login_manager.init_app(app)

    # register blueprints
    app.register_blueprint(file_api)
    app.register_blueprint(website)
    app.register_blueprint(users)
    app.register_blueprint(file_view)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=8080)
