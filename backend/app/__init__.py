from flask import Flask
from dotenv import load_dotenv

from app import models
from app.database.initializer import initialize_database

load_dotenv()

from app.config.settings import Settings
from app.extensions import cors, jwt, db
from app.modules.health.route import health_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Settings)

    if not app.config["JWT_SECRET_KEY"]:
        raise RuntimeError("JWT_SECRET_KEY must be configured")

    initialize_database()
    db.init_app(app)
    jwt.init_app(app)

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": [app.config["FRONTEND_ORIGIN"]]
            }
        },
    )

    app.register_blueprint(health_bp)

    return app
