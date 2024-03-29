import os
import json

import pytest

import app.config_test as config_test
from app import app, db


@pytest.fixture(scope="session")
def app():

    app.config.from_object(config_test)
    app.config["BACKEND_IP"] = "/api/v1"
    db.init_app(app)

    abs_file_path = os.path.abspath(os.path.dirname(__file__))
    openapi_path = os.path.join(abs_file_path, "../app/", "openapi")
    os.environ["SPEC_PATH"] = openapi_path

    return app


@pytest.fixture(scope="session", autouse=True)
def clean_up():
    yield
    default_pets = {
        "1": {"name": "ginger", "breed": "bengal", "price": 100},
        "2": {"name": "sam", "breed": "husky", "price": 10},
        "3": {"name": "guido", "breed": "python", "price": 518},
    }

    abs_file_path = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(abs_file_path, "../app/", "test_api", "core", "pets.json")
    with open(json_path, "w") as pet_store:
        json.dump(default_pets, pet_store, indent=4)
