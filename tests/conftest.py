import pytest
from flask import template_rendered
from server import app


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
