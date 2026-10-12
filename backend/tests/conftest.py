
import os

import pytest

from app import create_app
from app.extensions import db

from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def app():
    test_database_uri = os.getenv("TEST_DATABASE_URI")

    if not test_database_uri:
        pytest.fail(
            "TEST_DATABASE_URI must point to a dedicated test database."
        )

    flask_app = create_app(
        {
            "TESTING": True,
            "JWT_SECRET_KEY": "test-secret-key-not-for-production",
            "SQLALCHEMY_DATABASE_URI": test_database_uri,
            "INITIALIZE_DATABASE": False,
        }
    )

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()
