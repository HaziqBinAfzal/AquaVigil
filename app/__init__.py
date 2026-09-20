import os
import secrets

from flask import Flask

from .db import init_db
from .routes import bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("AQUAVIGIL_SECRET_KEY") or secrets.token_hex(32),
        DATABASE="instance/aquavigil.db",
        MAX_CONTENT_LENGTH=4 * 1024 * 1024,
        RESET_ON_START=os.getenv("AQUAVIGIL_RESET_ON_START", "0") == "1",
    )
    if test_config:
        app.config.update(test_config)
    app.register_blueprint(bp)
    init_db(app, reset=app.config["RESET_ON_START"] and not test_config)
    return app
