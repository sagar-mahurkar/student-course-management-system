from flask import Flask
from dotenv import load_dotenv

from app import models
from app.database.initializer import initialize_database
from app.seeders.admin_seeder import seed_admin

load_dotenv()

from app.config.settings import Settings
from app.extensions import cors, jwt, db
from app.errors.handlers import register_error_handlers
from app.modules.health.route import health_bp
from app.modules.auth.route import auth_bp
from app.modules.courses.route import courses_bp
from app.modules.enrollments.route import enrollments_bp
from app.modules.dashboard.route import dashboard_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Settings)

    if test_config:
        app.config.update(test_config)

    if not app.config["JWT_SECRET_KEY"]:
        raise RuntimeError("JWT_SECRET_KEY must be configured")

    db.init_app(app)
    jwt.init_app(app)

    if app.config.get("INITIALIZE_DATABASE", True):
        initialize_database()

        with app.app_context():
            db.create_all()
            seed_admin(app.config)

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": [app.config["FRONTEND_ORIGIN"]]
            }
        },
    )

    register_error_handlers(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(enrollments_bp)
    app.register_blueprint(dashboard_bp)

    return app
