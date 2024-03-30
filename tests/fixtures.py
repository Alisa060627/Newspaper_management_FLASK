
import pytest

from src.app import create_app
from src.model.agency import Agency
from tests.testdata import populate
from src.model.issue import Issue
from src.model.editor import Editor


@pytest.fixture()
def app():
    yield create_app()


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def agency(app):
    agency = Agency.get_instance()
    populate(agency)
    yield agency

