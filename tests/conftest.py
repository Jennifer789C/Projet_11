import pytest
from flask import template_rendered
from server import app
import server


@pytest.fixture()
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture()
def templates_utilises():
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture()
def club(mocker):
    club = mocker.patch.object(server, "clubs", [{"name": "Club test", "email": "mail@test.com", "points": "13"}])
    return club


@pytest.fixture()
def competitions(mocker):
    competitions = mocker.patch.object(server, "competitions", [{"name": "Competition test",
                                                                 "date": "2023-12-21 10:00:00",
                                                                 "numberOfPlaces": "25"}])
    return competitions


@pytest.fixture()
def reservations(mocker):
    reservations = mocker.patch.object(server, "reservations", [])
    return reservations
