from flask import Flask, current_app
from stock_service import api


def create_app(testing=False):
    app = Flask("stock_service")
    app.config.from_object("stock_service.config")

    if testing is True:
        app.config["TESTING"] = True

    register_blueprints(app)

    return app


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)


if __name__ == '__main__':
    app = create_app(False)
    HOST_URL = current_app.config['FLASK_RUN_HOST']
    HOST_PORT = current_app.config['FLASK_RUN_PORT']

    app.run(host=HOST_URL, port=HOST_PORT)
